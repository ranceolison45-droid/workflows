"""
StormBuster Backend API
FastAPI backend for storm damage analysis and lead generation
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime

from ai_chat_integration import StormBusterAIChat, AIProvider

# Initialize FastAPI app
app = FastAPI(
    title="StormBuster API",
    description="Storm damage analysis and lead generation API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Chat
ai_chat = StormBusterAIChat()

# ==================================================================
# Pydantic Models
# ==================================================================

class ChatRequest(BaseModel):
    message: str
    model_id: str = "gpt-3.5-turbo"
    subscription_tier: str = "basic"
    context: Optional[str] = None

class ChatResponse(BaseModel):
    success: bool
    response: Optional[str] = None
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None
    cost: Optional[float] = None
    timestamp: Optional[str] = None
    error: Optional[str] = None

class StormAnalysisRequest(BaseModel):
    date: str
    location: str
    hail_size: str
    property_count: int
    avg_property_value: Optional[str] = None

class LeadData(BaseModel):
    owner_name: str
    address: str
    property_value: Optional[str] = None
    storm_date: str
    hail_size: str
    phone: Optional[str] = None

class HealthCheck(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, str]

# ==================================================================
# API Routes
# ==================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "StormBuster API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/models": "Available AI models",
            "/chat": "Send chat message",
            "/analyze-storm": "Analyze storm data",
            "/generate-lead-insights": "Generate lead insights"
        }
    }

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    services = {}
    
    # Check AI providers
    providers = ["OPENAI", "ANTHROPIC", "GOOGLE"]
    for provider in providers:
        provider_enum = AIProvider[provider]
        services[provider] = "available" if provider_enum in ai_chat.providers else "unavailable"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": services
    }

@app.get("/models")
async def get_models(tier: str = "basic"):
    """Get available AI models for subscription tier"""
    try:
        models = ai_chat.get_available_models(tier)
        return {
            "success": True,
            "tier": tier,
            "models": models
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a chat message to AI"""
    try:
        result = ai_chat.send_message(
            message=request.message,
            model_id=request.model_id,
            subscription_tier=request.subscription_tier,
            context=request.context
        )
        return ChatResponse(**result)
    except Exception as e:
        return ChatResponse(
            success=False,
            error=str(e)
        )

@app.post("/analyze-storm")
async def analyze_storm(request: StormAnalysisRequest):
    """Analyze storm data using AI"""
    try:
        storm_data = request.dict()
        result = ai_chat.analyze_storm_data(
            storm_data=storm_data,
            model_id="gpt-4"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-lead-insights")
async def generate_lead_insights(lead_data: LeadData):
    """Generate insights for individual leads"""
    try:
        result = ai_chat.generate_lead_insights(
            lead_data=lead_data.dict(),
            model_id="claude-3"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat-history")
async def get_chat_history(limit: int = 50):
    """Get chat history"""
    try:
        history = ai_chat.get_chat_history(limit)
        return {
            "success": True,
            "history": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/chat-history")
async def clear_chat_history():
    """Clear chat history"""
    try:
        ai_chat.clear_chat_history()
        return {"success": True, "message": "Chat history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/usage-stats")
async def get_usage_stats(tier: str = "basic"):
    """Get usage statistics"""
    try:
        stats = ai_chat.get_usage_stats(tier)
        return {
            "success": True,
            "tier": tier,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export-chat")
async def export_chat():
    """Export chat history as JSON"""
    try:
        export_data = ai_chat.export_chat_history()
        return {
            "success": True,
            "data": export_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================================================================
# Run Server
# ==================================================================

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

