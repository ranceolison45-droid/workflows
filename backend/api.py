#!/usr/bin/env python3
"""
DFW Hail Pipeline - FastAPI Backend
RESTful API for hail damage property identification
"""
import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import pandas as pd
import uvicorn

# Add parent directory to path to import dfw_pipeline
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
os.chdir(parent_dir)  # Change to project root for file access

# Import PropertyMatcher directly to avoid package init dependencies
import importlib.util
spec = importlib.util.spec_from_file_location(
    "property_matcher",
    parent_dir / "dfw_pipeline" / "core" / "property_matcher.py"
)
property_matcher_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(property_matcher_module)
PropertyMatcher = property_matcher_module.PropertyMatcher

# Initialize FastAPI app
app = FastAPI(
    title="DFW Hail Pipeline API",
    description="API for identifying hail-damaged properties in DFW area",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_DIR = parent_dir / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR = parent_dir / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


# Pydantic models
class PropertyMatchConfig(BaseModel):
    min_hail_size_in: float = 1.0
    base_radius_mi: float = 1.0
    radius_per_inch_mi: float = 1.0
    max_radius_mi: float = 5.0


class MatchResponse(BaseModel):
    success: bool
    message: str
    output_file: Optional[str] = None
    total_properties: Optional[int] = None
    damaged_properties: Optional[int] = None
    hail_events: Optional[int] = None


class StatsResponse(BaseModel):
    total_properties: int
    damaged_properties: int
    hail_events: int
    damage_percentage: float


# Initialize property matcher
matcher = PropertyMatcher()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "DFW Hail Pipeline API",
        "version": "1.0.0",
        "endpoints": {
            "GET /api/stats": "Get statistics",
            "POST /api/match": "Run property matching",
            "GET /api/results/{filename}": "Download results CSV"
        }
    }


@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """Get statistics about current data"""
    try:
        # Load hail events
        hail = matcher.load_hail_events()
        
        # Load properties
        props = matcher.load_property_lookups()
        
        # Quick match to get stats
        scored = matcher.compute_damage_matches(props.head(1000), hail.head(100))  # Sample for speed
        damaged = scored[scored["hail_damage_likely"]].shape[0]
        
        # Estimate for full dataset
        damage_rate = damaged / len(scored) if len(scored) > 0 else 0
        estimated_damaged = int(len(props) * damage_rate)
        
        return StatsResponse(
            total_properties=len(props),
            damaged_properties=estimated_damaged,
            hail_events=len(hail),
            damage_percentage=round(damage_rate * 100, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/match", response_model=MatchResponse)
async def match_properties(
    config: PropertyMatchConfig = PropertyMatchConfig(),
    background_tasks: BackgroundTasks = None
):
    """Run property matching with hail events"""
    try:
        # Update matcher config
        matcher.min_hail_size_in = config.min_hail_size_in
        matcher.base_radius_mi = config.base_radius_mi
        matcher.radius_per_inch_mi = config.radius_per_inch_mi
        matcher.max_radius_mi = config.max_radius_mi
        
        # Load data
        hail = matcher.load_hail_events()
        props = matcher.load_property_lookups()
        
        # Compute matches
        scored = matcher.compute_damage_matches(props, hail)
        
        # Select key columns
        keep_cols = [
            c for c in [
                "property_address", "city", "COUNTY", "postcode", "prop_lat", "prop_lon",
                "owner_name", "owner_mailing_address", "property_type", "year_built",
                "appraisal_value", "account_number", "data_source", "lookup_url",
                "nearest_hail_miles", "nearest_hail_size_in", "hail_damage_likely", "__source_file"
            ] if c in scored.columns
        ]
        out = scored[keep_cols].copy()
        out.sort_values(["hail_damage_likely", "nearest_hail_miles"], ascending=[False, True], inplace=True)
        
        # Save output
        output_file = OUTPUT_DIR / "hail_damaged_properties.csv"
        out.to_csv(output_file, index=False)
        
        damaged_count = out[out["hail_damage_likely"]].shape[0]
        
        return MatchResponse(
            success=True,
            message=f"Successfully matched {len(out):,} properties",
            output_file=str(output_file),
            total_properties=len(out),
            damaged_properties=damaged_count,
            hail_events=len(hail)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/results/{filename}")
async def download_results(filename: str):
    """Download results CSV file"""
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/csv"
    )


@app.get("/api/properties")
async def get_properties(
    limit: int = 100,
    offset: int = 0,
    damaged_only: bool = False
):
    """Get properties with pagination"""
    try:
        # Check if results file exists
        results_file = OUTPUT_DIR / "hail_damaged_properties.csv"
        if results_file.exists():
            df = pd.read_csv(results_file)
        else:
            # Run quick match
            hail = matcher.load_hail_events()
            props = matcher.load_property_lookups()
            scored = matcher.compute_damage_matches(props, hail)
            df = scored
        
        if damaged_only:
            df = df[df.get("hail_damage_likely", False)]
        
        # Paginate
        total = len(df)
        df_page = df.iloc[offset:offset + limit]
        
        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "properties": df_page.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "DFW Hail Pipeline API"}


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

