# API Reference

This document provides detailed information about the main classes and functions in the Sentinel-2 Water Quality Processing Toolkit.

## Main Workflow Script

### `run_workflow.py`

The main entry point for the toolkit.

#### Command Line Arguments

```bash
python run_workflow.py [OPTIONS]
```

**Options:**
- `--config PATH`: Configuration file path (default: `02_config/parameters.yaml`)
- `--action {download,process,plot,full}`: Action to perform (default: `full`)
- `--start-date YYYY-MM-DD`: Start date for processing
- `--end-date YYYY-MM-DD`: End date for processing
- `--clean`: Clean processed data before processing
- `--setup`: Setup directory structure

**Examples:**
```bash
# Full workflow with specific dates
python run_workflow.py --action full --start-date 2025-05-15 --end-date 2025-05-16

# Download only
python run_workflow.py --action download --start-date 2025-05-15 --end-date 2025-05-16

# Process with clean start
python run_workflow.py --action process --clean
```

## Core Classes

### `Sentinel2Downloader`

Handles downloading Sentinel-2 data from the Copernicus Data Space Ecosystem.

#### Constructor
```python
from download import Sentinel2Downloader

downloader = Sentinel2Downloader(config_path)
```

**Parameters:**
- `config_path` (str): Path to configuration YAML file

#### Methods

##### `download_products(start_date, end_date)`
Download Sentinel-2 products for the specified date range.

**Parameters:**
- `start_date` (datetime): Start date for download
- `end_date` (datetime): End date for download

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
from datetime import datetime
downloader = Sentinel2Downloader('02_config/parameters.yaml')
success = downloader.download_products(
    datetime(2025, 5, 15),
    datetime(2025, 5, 16)
)
```

##### `search_products(start_date, end_date)`
Search for available products without downloading.

**Parameters:**
- `start_date` (datetime): Start date for search
- `end_date` (datetime): End date for search

**Returns:**
- `list`: List of available products

### `WaterQualityProcessor`

Handles the complete processing pipeline using SNAP.

#### Constructor
```python
from process_pipeline import WaterQualityProcessor

processor = WaterQualityProcessor(config_path)
```

**Parameters:**
- `config_path` (str): Path to configuration YAML file

#### Methods

##### `run_full_pipeline(start_date=None, end_date=None)`
Run the complete processing pipeline.

**Parameters:**
- `start_date` (datetime, optional): Filter processing by start date
- `end_date` (datetime, optional): Filter processing by end date

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
processor = WaterQualityProcessor('02_config/parameters.yaml')
success = processor.run_full_pipeline()
```

##### `process_l2a(input_file, output_file)`
Process L1C to L2A (atmospheric correction).

**Parameters:**
- `input_file` (str): Path to input L1C file
- `output_file` (str): Path to output L2A file

**Returns:**
- `bool`: True if successful, False otherwise

##### `resample_and_subset(input_file, output_file)`
Resample and subset the data.

**Parameters:**
- `input_file` (str): Path to input file
- `output_file` (str): Path to output file

**Returns:**
- `bool`: True if successful, False otherwise

##### `reproject_data(input_file, output_file)`
Reproject data to target CRS.

**Parameters:**
- `input_file` (str): Path to input file
- `output_file` (str): Path to output file

**Returns:**
- `bool`: True if successful, False otherwise

##### `apply_c2rcc(input_file, output_file)`
Apply C2RCC atmospheric correction and water quality parameter extraction.

**Parameters:**
- `input_file` (str): Path to input file
- `output_file` (str): Path to output file

**Returns:**
- `bool`: True if successful, False otherwise

### `WaterQualityPlotter`

Handles visualization and plotting of water quality data.

#### Constructor
```python
from plotting import WaterQualityPlotter

plotter = WaterQualityPlotter(config_path)
```

**Parameters:**
- `config_path` (str): Path to configuration YAML file

#### Methods

##### `generate_all_plots(start_date=None, end_date=None)`
Generate all plots for processed data.

**Parameters:**
- `start_date` (datetime, optional): Filter plots by start date
- `end_date` (datetime, optional): Filter plots by end date

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
plotter = WaterQualityPlotter('02_config/parameters.yaml')
success = plotter.generate_all_plots()
```

##### `plot_water_quality_parameter(data_file, parameter, output_file)`
Plot a specific water quality parameter.

**Parameters:**
- `data_file` (str): Path to NetCDF data file
- `parameter` (str): Parameter name ('chl', 'tsm', 'cdom')
- `output_file` (str): Path to output PNG file

**Returns:**
- `bool`: True if successful, False otherwise

##### `plot_rgb_composite(data_file, output_file)`
Create RGB composite image.

**Parameters:**
- `data_file` (str): Path to data file
- `output_file` (str): Path to output PNG file

**Returns:**
- `bool`: True if successful, False otherwise

## Utility Functions

### `utils.py`

Contains utility functions for the toolkit.

#### Functions

##### `setup_logging(log_file=None, level=logging.INFO)`
Setup logging configuration.

**Parameters:**
- `log_file` (str, optional): Path to log file
- `level` (int): Logging level

**Example:**
```python
from utils import setup_logging
setup_logging('processing.log', logging.DEBUG)
```

##### `create_directory_structure(base_path)`
Create the complete directory structure.

**Parameters:**
- `base_path` (str): Base path for directory structure

##### `validate_snap_installation()`
Validate SNAP installation.

**Returns:**
- `bool`: True if SNAP is properly installed, False otherwise

##### `validate_python_dependencies()`
Validate Python dependencies.

**Returns:**
- `bool`: True if all dependencies are installed, False otherwise

##### `clean_processed_data(base_path)`
Clean processed data directories.

**Parameters:**
- `base_path` (str): Base path of the project

##### `print_processing_statistics(base_path)`
Print processing statistics.

**Parameters:**
- `base_path` (str): Base path of the project

## Configuration File Structure

The main configuration file (`02_config/parameters.yaml`) has the following structure:

```yaml
# Study Area Configuration
study_area:
  name: str                    # Name of the study area
  wkt_geometry: str           # WKT polygon geometry
  subset_geometry: str        # Subset geometry (optional)
  epsg_code: int             # EPSG code for CRS

# Data Download Configuration
download:
  copernicus_user: str        # Copernicus username
  copernicus_password: str    # Copernicus password
  data_collection: str        # Data collection name
  product_type: str          # Product type (L1C, L2A)
  cloud_cover_threshold: int  # Maximum cloud cover percentage
  default_start_date: str    # Default start date (YYYY-MM-DD)
  default_end_date: str      # Default end date (YYYY-MM-DD)

# Processing Parameters
processing:
  target_resolution: int      # Target resolution in meters
  target_crs: str            # Target coordinate reference system
  subset_to_study_area: bool # Whether to subset to study area

# L2A Processing
l2a:
  atmospheric_correction: bool # Enable atmospheric correction
  cirrus_correction: bool     # Enable cirrus correction

# C2RCC Parameters
c2rcc:
  atmospheric_correction: bool # Enable atmospheric correction
  derive_rwn: bool           # Derive remote sensing reflectance
  output_uncertainties: bool  # Output uncertainty estimates
  salinity: float            # Water salinity (PSU)
  temperature: float         # Water temperature (°C)
  ozone: float              # Atmospheric ozone (DU)
  press: float              # Atmospheric pressure (hPa)

# Output Parameters
output:
  create_rgb: bool           # Create RGB composite
  create_water_quality_maps: bool # Create water quality maps
  output_format: str         # Output format (NetCDF, GeoTIFF)
  create_png_outputs: bool   # Create PNG outputs

# Visualization Parameters
visualization:
  dpi: int                   # Output DPI for images
  figure_size: list          # Figure size [width, height]
  colormap_chl: str          # Colormap for chlorophyll
  colormap_tsm: str          # Colormap for TSM
  colormap_cdom: str         # Colormap for CDOM

# Quality Control
quality_control:
  mask_clouds: bool          # Mask cloudy pixels
  mask_land: bool           # Mask land pixels
  mask_invalid_pixels: bool  # Mask invalid pixels

# File Management
file_management:
  keep_intermediate_files: bool # Keep intermediate processing files
  compress_outputs: bool     # Compress output files
  cleanup_raw_data: bool     # Clean up raw data after processing
```

## Error Handling

All main functions return boolean values indicating success or failure. Detailed error messages are logged to:

- Console output
- Log files in `06_logs/`

Common error patterns:

```python
try:
    success = processor.run_full_pipeline()
    if not success:
        logger.error("Processing failed")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

## Data Formats

### Input Data
- **Sentinel-2 L1C**: ZIP files from Copernicus
- **Configuration**: YAML files

### Intermediate Data
- **L2A Products**: BEAM-DIMAP format (.dim files)
- **NetCDF Files**: Scientific data format (.nc files)

### Output Data
- **PNG Images**: Visualization outputs
- **NetCDF Files**: Scientific data with water quality parameters
- **Log Files**: Processing information

## Performance Considerations

- **Memory Usage**: Processing requires 4-8GB RAM per scene
- **Disk Space**: Allow 2-5GB per scene for intermediate files
- **Processing Time**: 10-30 minutes per scene depending on system

## Thread Safety

The toolkit is designed for single-threaded operation. For parallel processing of multiple scenes, run separate instances with different configuration files.

## Version Information

Check version information:
```python
import sys
print(f"Python: {sys.version}")
print(f"Toolkit: See README.md for version")
```
