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
│       ├── cdom_band_math.xml     # CDOM calculation graph
│       └── rgb_profile_s2.rgb     # RGB profile for true color
│
├── 03_raw_data/                   # Downloaded raw data
│   └── sentinel2_l1c/             # Sentinel-2 L1C zip files
│
├── 04_processed_data/             # Intermediate processed data
│   ├── l2a_resampled/             # Resampled and subset data
│   ├── l2a_reprojected/           # Reprojected data
│   ├── c2rcc_output/              # C2RCC processed data
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
- Outputs NetCDF format

### Step 6: CDOM Calculation
- Calculates CDOM using band math on atmospherically corrected data
- Uses empirical algorithm with reflectance bands
- Outputs NetCDF format

### Step 7: Visualization
- Generates publication-ready plots
- Applies custom colormaps for each parameter
- Outputs high-resolution PNG files

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

# Process data
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml

# Generate plots
python 01_scripts/plotting.py --config 02_config/parameters.yaml
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
