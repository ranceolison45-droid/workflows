            ipeline - Python Package

A comprehensive, Python-compatible package for collecting, processing, and .analyzing hail events in the DFW (Dallas-Fort Worth) area.

## Features

- **Data Collection**: Downloads hail event data from NOAA Storm Events database
- **Geocoding**: Reverse geocodes events to add city/neighborhood information
- **Property Matching**: Matches properties with hail events using geospatial proximity
- **Unified API**: Clean, object-oriented interface for all pipeline operations
- **PowerShell Compatible**: Includes PowerShell scripts for easy execution

## Installation

The package is already included in this project. No additional installation needed if you're using the project's virtual environment.

## Quick Start

### Python Usage

```python
from dfw_pipeline import DFWPipelineRunner

# Initialize runner
runner = DFWPipelineRunner("config.yaml")

# Run full pipeline
results = runner.run_full_pipeline()

# Or run individual steps
runner.collect_data()  # Step 1: Collect from NOAA
runner.geocode_data()   # Step 2: Add geocoding
runner.match_properties()  # Step 3: Match properties
```

### Command Line Usage

```bash
# Run full pipeline
python run_dfw_pipeline.py

# Only collect data
python run_dfw_pipeline.py --collect-only

# Skip geocoding
python run_dfw_pipeline.py --no-geocode

# Only match properties
python run_dfw_pipeline.py --match-only
```

### PowerShell Usage

```powershell
# Run full pipeline
.\run_dfw_pipeline.ps1

# Only collect data
.\run_dfw_pipeline.ps1 -CollectOnly

# Skip geocoding
\run_dfw_pipeline.ps1 -NoGeocode

# Only match properties
.\run_dfw_pipeline.ps1 -MatchOnly
```

## Package Structure

```
dfw_pipeline/
├── __init__.py              # Package initialization
├── core/
│   ├── __init__.py
│   ├── data_collector.py    # NOAA data collection
│   ├── geocoder.py          # Reverse geocoding
│   ├── property_matcher.py  # Property matching
│   └── pipeline_runner.py    # Unified runner
└── README.md                # This file
```

## Components

### HailDataCollector

Downloads and processes hail event data from NOAA.

```python
from dfw_pipeline.core.data_collector import HailDataCollector

collector = HailDataCollector("config.yaml")
df = collector.process_and_save("output.csv")
```

### HailGeocoder

Adds city/neighborhood information to hail events.

```python
from dfw_pipeline.core.geocoder import HailGeocoder

geocoder = HailGeocoder(email="your-email@example.com", delay=1.2)
enriched_df = geocoder.geocode_dataframe(df)
```

### PropertyMatcher

Matches properties with hail events based on proximity.

```python
from dfw_pipeline.core.property_matcher import PropertyMatcher

matcher = PropertyMatcher(
    min_hail_size_in=1.0,
    base_radius_mi=1.0,
    radius_per_inch_mi=1.0,
    max_radius_mi=5.0
)
matched_df = matcher.process("output.csv")
```

### DFWPipelineRunner

Unified interface for running the complete pipeline.

```python
from dfw_pipeline import DFWPipelineRunner

runner = DFWPipelineRunner("config.yaml")
results = runner.run_full_pipeline()
```

## Configuration

The pipeline uses `config.yaml` for configuration. Key settings:

```yaml
years:
  - 2024
  - 2025
state_fips: '48'
dfw_counties:
  - Collin
  - Dallas
  - Denton
  # ... more counties
output_csv: hail_events_dfw_2024_2025.csv
geocode_output_csv: hail_events_dfw_2024_2025_neighborhoods.csv
reverse_geocode:
  enabled: true
  email_contact: your-email@example.com
  sleep_seconds: 1.2
```

## Output Files

The pipeline generates several output files:

1. **hail_events_dfw_2024_2025.csv** - Raw hail events data
2. **hail_events_dfw_2024_2025_neighborhoods.csv** - Geocoded events (if enabled)
3. **hail_damaged_properties.csv** - Properties matched with hail events

## Integration with Flask App

The pipeline can be integrated into the Flask application:

```python
from dfw_pipeline import DFWPipelineRunner

@app.route('/api/run-pipeline', methods=['POST'])
def run_pipeline():
    runner = DFWPipelineRunner()
    results = runner.run_full_pipeline()
    return jsonify(results)
```

## Requirements

- Python 3.8+
- pandas
- requests
- pyyaml
- geopy (for geocoding)
- tqdm (optional, for progress bars)

All dependencies are included in `requirements.txt`.

## License

Part of the StormBuster project.


us