# Sentinel-2 Water Quality Processing - Workflow Documentation

## Overview

This document provides detailed technical information about the Sentinel-2 water quality processing workflow. For quick start instructions, see the main [README.md](../README.md).

The system processes Sentinel-2 satellite imagery to extract water quality parameters including Chlorophyll-a (CHL), Total Suspended Matter (TSM), and Colored Dissolved Organic Matter (CDOM) using the C2RCC atmospheric correction algorithm.

## Table of Contents

1. [Detailed Directory Structure](#detailed-directory-structure)
2. [Technical Configuration](#technical-configuration)
3. [Processing Pipeline Details](#processing-pipeline-details)
4. [Advanced Usage](#advanced-usage)
5. [Algorithm Details](#algorithm-details)
6. [File Formats and Outputs](#file-formats-and-outputs)
7. [Performance Optimization](#performance-optimization)

## Detailed Directory Structure

The workflow uses a comprehensive directory structure for organized processing:

```
Sentinel2_WQ/
├── 01_scripts/                    # All processing scripts
│   ├── download.py                # Data download script
│   ├── process_pipeline.py        # Main processing pipeline
│   ├── plotting.py                # Visualization script
│   └── utils.py                   # Utility functions
│
├── 02_config/                     # Configuration files
│   ├── parameters.yaml            # Main configuration
│   └── snap_graphs/               # SNAP processing graphs
│       ├── resample_subset.xml    # Resample and subset graph
│       ├── reproject.xml          # Reprojection parameters
│       ├── c2rcc_param.xml        # C2RCC parameters
│       ├── mosaic.xml             # Mosaic parameters (for multiple tiles)
│       ├── cdom_band_math.xml     # CDOM calculation graph
│       └── rgb_profile_s2.rgb     # RGB profile for true color
│
├── 03_raw_data/                   # Downloaded raw data
│   └── sentinel2_l1c/             # Sentinel-2 L1C zip files
│
├── 04_processed_data/             # Intermediate processed data
│   ├── l2a_resampled/             # Resampled and subset data
│   ├── l2a_reprojected/           # Reprojected data
│   ├── c2rcc_output/              # C2RCC processed data (single tiles)
│   ├── mosaic_output/             # Mosaicked data (multiple tiles)
│   └── cdom_output/               # CDOM calculated data
│
├── 05_final_products/             # Final output products
│   ├── chl/                       # Chlorophyll-a maps
│   ├── tsm/                       # Total Suspended Matter maps
│   ├── cdom/                      # CDOM maps
│   └── true_color/                # True color images
│
├── 06_logs/                       # Processing logs
├── 07_documentation/              # Documentation and metadata
├── requirements.txt               # Python dependencies
├── run_workflow.py                # Master workflow script
├── run_workflow.bat               # Windows batch script
└── workflow_demo.ipynb            # Jupyter notebook demo
```

## Study Area Configuration

### Setting Up Your Study Area

The workflow automatically configures all SNAP processing tools based on your study area geometry. You only need to update one place:

**File**: `02_config/parameters.yaml`

```yaml
study_area:
  name: "Your Study Area Name"
  wkt_geometry: "POLYGON ((lon1 lat1, lon2 lat2, lon3 lat3, lon4 lat4, lon1 lat1))"
```

### How It Works

1. **Single Point of Configuration**: Update the `wkt_geometry` in parameters.yaml
2. **Automatic Propagation**: The workflow automatically:
   - Extracts bounds from your WKT polygon
   - Updates all SNAP XML graph files
   - Applies geometry to resampling, subsetting, and reprojection operations
   - Maintains consistency across all processing steps

### Geographic Coordinates Format

The WKT geometry should be a closed polygon with coordinates in **(longitude, latitude)** order:

```
POLYGON ((lon1 lat1, lon2 lat2, lon3 lat3, lon4 lat4, lon1 lat1))
```

Example for Western Australia:
```
POLYGON ((115.54 -31.93, 115.79 -31.93, 115.79 -32.26, 115.54 -32.26, 115.54 -31.93))
```

### Manual Update (if needed)

To manually update SNAP geometry files without running the full pipeline:

```bash
python 01_scripts/update_snap_geometry.py --config 02_config/parameters.yaml
```

This will:
- Read the WKT geometry from parameters.yaml
- Extract geographic bounds
- Update all relevant SNAP XML files
- Report which files were updated

## Technical Configuration

**For basic setup instructions, see the main [README.md](../README.md) and [GETTING_STARTED.md](GETTING_STARTED.md)**

### Main Configuration File: `02_config/parameters.yaml`

```yaml
# Study Area Configuration
study_area:
  name: "Western Australia Coast"
  wkt_geometry: "POLYGON ((115.54 -31.93, 115.79 -31.93, 115.78 -32.26, 115.53 -32.26, 115.54 -31.93))"
  subset_geometry: "POLYGON ((115.40 -31.95, 115.80 -31.95, 115.80 -32.30, 115.40 -32.30, 115.40 -31.95))"

# Data Download Configuration
download:
  copernicus_user: "your_username@email.com"
  copernicus_password: "your_password"
  cloud_cover_threshold: 10
  default_start_date: "2025-05-01"
  default_end_date: "2025-06-30"

# Processing Parameters
processing:
  c2rcc:
    salinity: 35.0
    temperature: 30.0
    valid_pixel_expression: "B8 > 0 && B8 < 0.1"
  
  cdom:
    expression: "exp(0.544 * log(rhown_B1)-0.571 * log(rhown_B2)-2.181*log(rhown_B3)+1.398*log(rhown_B4)-1.406)"
```

## Workflow Steps

### Step 1: Data Download
Downloads Sentinel-2 L1C data from Copernicus Data Space Ecosystem based on:
- Date range
- Study area boundary
- Cloud cover threshold
- Product type (L1C)

### Step 2: Resample and Subset
- Resamples all bands to 10m resolution using B2 as reference
- Subsets data to study area extent
- Outputs BEAM-DIMAP format

### Step 3: Reproject
- Reprojects data to WGS84 coordinate system
- Maintains spatial resolution and extent

### Step 4: True Color Generation
- Generates RGB true color images
- Uses predefined RGB profile for Sentinel-2
- Outputs PNG format

### Step 5: C2RCC Processing
- Applies Case-2 Regional Coast Color atmospheric correction
- Calculates water quality parameters (CHL, TSM)
- Processes each tile individually
- Outputs NetCDF format to `c2rcc_output/`

### Step 6: Mosaic Processing (Conditional)
**Intelligent multi-tile handling:**
- **Multiple tiles for same date**: Automatically creates mosaic
  - Combines tiles into single seamless dataset
  - Outputs to `mosaic_output/`
  - Used for subsequent processing
- **Single tile**: Skips mosaic processing
  - Directly uses C2RCC output for water quality calculation
  - Saves processing time and disk space

### Step 7: CDOM Calculation
- Calculates CDOM using band math on atmospherically corrected data
- **Adapts to data source**: Automatically uses mosaic if available, otherwise C2RCC
- Uses empirical algorithm with reflectance bands
- Outputs NetCDF format

### Step 8: Visualization
- Generates publication-ready plots
- Applies custom colormaps for each parameter
- Reads from both C2RCC and mosaic outputs as needed
- Outputs high-resolution PNG files

## Multi-tile and Single-tile Handling

The workflow intelligently adapts to study area coverage:

### Single-tile Scenarios
When your study area falls entirely within a single Sentinel-2 tile:
```
Input: 1 C2RCC file per date
Flow: C2RCC → CDOM Calculation → Plotting
Output:
  - No mosaic created (saves ~30-50% disk space)
  - Faster processing (no mosaic time required)
  - Direct output to final products
```

### Multi-tile Scenarios
When your study area spans multiple Sentinel-2 tiles:
```
Input: Multiple C2RCC files per date (e.g., 2-4 tiles)
Flow: C2RCC → Mosaic → CDOM Calculation → Plotting
Output:
  - Mosaicked dataset in mosaic_output/
  - Single seamless product for each date
  - Consistent spatial coverage across tiles
```

### Automatic Detection
The workflow automatically:
1. Groups C2RCC outputs by date
2. Counts tiles per date (determined by processing all input imagery)
3. For single-tile dates: skips mosaic, processes directly
4. For multi-tile dates: creates mosaic, then processes
5. CDOM calculation adapts to available source (mosaic or c2rcc)
6. Plotting reads from both directories as needed

## Usage Examples

### Complete Workflow
```bash
# Run complete workflow
python run_workflow.py --action full

# Run with specific date range
python run_workflow.py --action full --start-date 2025-05-01 --end-date 2025-06-30

# Run with cleaning previous processed data
python run_workflow.py --action full --clean
```

### Individual Steps
```bash
# Download data only
python run_workflow.py --action download --start-date 2025-05-01 --end-date 2025-06-30

# Process data only
python run_workflow.py --action process

# Generate plots only
python run_workflow.py --action plot
```

### Using Individual Scripts
```bash
# Download data
python 01_scripts/download.py --config 02_config/parameters.yaml

# Process data (full pipeline)
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml

# Process individual steps (use --step flag with numbers 1-7)
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 1  # Resample and Subset
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 2  # Reproject
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 3  # True Color
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 4  # C2RCC
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 5  # Mosaic (if needed)
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 6  # CDOM Calculation
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 7  # Generate Plots

# Generate plots
python 01_scripts/plotting.py --config 02_config/parameters.yaml --parameter all  # All parameters
python 01_scripts/plotting.py --config 02_config/parameters.yaml --parameter chl  # Chlorophyll only
python 01_scripts/plotting.py --config 02_config/parameters.yaml --parameter tsm  # TSM only
python 01_scripts/plotting.py --config 02_config/parameters.yaml --parameter cdom # CDOM only
```

## Fresh Repository Setup

For new users starting with a fresh repository:

```bash
python setup_fresh_repo.py
```

This will:
- Create the complete directory structure
- Set up configuration templates
- Create placeholder README files
- Prepare the repository for first use

After setup, configure your credentials:
```bash
# Edit configuration with your Copernicus credentials
# Update 02_config/parameters.yaml with your study area and credentials
```

## Troubleshooting

### Common Issues

1. **SNAP GPT not found**
   - Ensure SNAP is installed and `gpt` command is in PATH
   - Test with: `gpt --help`

2. **Python import errors**
   - Install missing packages: `pip install -r requirements.txt`
   - Check Python version: `python --version`

3. **Authentication errors**
   - Verify Copernicus credentials in configuration
   - Check internet connectivity

4. **Processing errors**
   - Check log files in `06_logs/`
   - Verify input data exists
   - Check disk space

### Log Files

Processing logs are stored in `06_logs/` with timestamps:
- `processing_YYYYMMDD_HHMMSS.log` - Processing pipeline logs
- `master_YYYYMMDD_HHMMSS.log` - Master workflow logs

## Technical Details

### Water Quality Parameters

1. **Chlorophyll-a (CHL)**
   - Units: mg/m³
   - Range: 0.01 - 20.0 mg/m³
   - Colormap: Custom 21-color scale
   - Source: C2RCC `conc_chl` variable

2. **Total Suspended Matter (TSM)**
   - Units: g/m³
   - Range: 0 - 4 g/m³
   - Colormap: cmocean turbid
   - Source: C2RCC `conc_tsm` variable

3. **Colored Dissolved Organic Matter (CDOM)**
   - Units: m⁻¹
   - Range: 0 - 4 m⁻¹
   - Colormap: YlOrBr
   - Source: Calculated using band math

### CDOM Algorithm

The CDOM algorithm uses the following empirical relationship:
```
CDOM = exp(0.544 * log(rhown_B1) - 0.571 * log(rhown_B2) - 2.181 * log(rhown_B3) + 1.398 * log(rhown_B4) - 1.406)
```

Where:
- `rhown_B1, B2, B3, B4` are water-leaving reflectances from C2RCC
- Coefficients are derived from regional calibration

### C2RCC Parameters

Key parameters for Australian coastal waters:
- Salinity: 35.0 psu
- Temperature: 30.0°C
- Valid pixel expression: `B8 > 0 && B8 < 0.1`
- TSM factor: 1.06
- CHL factor: 21.0

### Performance Optimization

1. **Parallel Processing**: SNAP operations use available CPU cores
2. **Memory Management**: Large datasets processed in chunks
3. **Disk I/O**: Intermediate files stored on fast storage
4. **Caching**: Processed data cached to avoid recomputation

## Quality Control

### Data Quality Checks

1. **Cloud Masking**: Products with >10% cloud cover excluded
2. **Valid Pixel Filtering**: Invalid pixels masked using C2RCC flags
3. **Range Validation**: Parameter values outside physical ranges excluded
4. **Spatial Consistency**: Obvious outliers identified and flagged

### Output Validation

1. **File Integrity**: NetCDF files checked for corruption
2. **Metadata Validation**: Ensure all required attributes present
3. **Statistical Summary**: Basic statistics logged for each parameter
4. **Visual Inspection**: Sample plots generated for quality assessment

## Future Enhancements

1. **Multi-temporal Analysis**: Time series analysis capabilities
2. **Machine Learning**: Advanced classification algorithms
3. **Real-time Processing**: Automated processing of new acquisitions
4. **Web Interface**: Browser-based visualization and analysis
5. **API Integration**: RESTful API for programmatic access

## References

1. Brockmann, C., et al. (2016). Evolution of the C2RCC Neural Network for Sentinel 2 and 3 for the Retrieval of Ocean Colour Products in Normal and Extreme Optically Complex Waters. Living Planet Symposium, Prague.

2. Doerffer, R. & Schiller, H. (2007). The MERIS Case 2 water algorithm. International Journal of Remote Sensing, 28(3-4), 517-535.

3. ESA (2015). Sentinel-2 User Handbook. European Space Agency.

## Support

For technical support and questions:
- Check documentation in `07_documentation/`
- Review log files in `06_logs/`
- Consult SNAP documentation: https://step.esa.int/main/doc/
- ESA Sentinel-2 resources: https://sentinel.esa.int/web/sentinel/missions/sentinel-2
