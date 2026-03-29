# Sentinel-2 Water Quality Processing Toolkit

A comprehensive, automated toolkit for processing Sentinel-2 satellite imagery to extract water quality parameters including Chlorophyll-a (CHL), Total Suspended Matter (TSM), and Colored Dissolved Organic Matter (CDOM).

## 🌊 Features

- **🎯 Study-Area Agnostic** - Update WKT geometry once, all SNAP XML files update automatically
- **🗺️ Intelligent Multi-tile Processing** - Automatically detects single vs multi-tile coverage:
  - Single-tile: Skips mosaic, saves ~30-50% disk space
  - Multi-tile: Automatically creates mosaics for seamless coverage
- **⚙️ Automated Data Download** from Copernicus Data Space Ecosystem
- **🔄 Complete Processing Pipeline** using SNAP and C2RCC algorithms
- **💧 Water Quality Parameter Extraction** (CHL, TSM, CDOM)
- **📊 Automated Visualization** with publication-ready plots
- **📁 Professional Directory Structure** with organized outputs
- **🛡️ Comprehensive Error Handling** and logging
- **⚡ Easy Configuration** via YAML files (no XML editing needed!)

## 📋 Prerequisites

### Software Requirements
- **Python 3.8+** (tested with Python 3.12)
- **SNAP (Sentinel Application Platform)** - [Download here](https://step.esa.int/main/download/snap-download/)
- **Git** (for cloning the repository)

### System Requirements
- **Operating System**: Windows 10/11, Linux, or macOS
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB+ free space for processing
- **Internet**: Required for data download

### Copernicus Account
- Create a free account at [Copernicus Data Space Ecosystem](https://identity.dataspace.copernicus.eu/)
- Note your email and password for configuration

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/ronygolderku/sentinel2-water-quality.git
cd sentinel2-water-quality
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install SNAP
1. Download SNAP from [ESA STEP](https://step.esa.int/main/download/snap-download/)
2. Install as Administrator (Windows) or with sudo (Linux/macOS)
3. Add SNAP to your system PATH:
   - **Windows**: Add `C:\Program Files\esa-snap\bin` to PATH
   - **Linux/macOS**: Add `/usr/local/snap/bin` to PATH

### 4. Quick Setup
```bash
python quick_setup.py
```
This will:
- Verify all dependencies
- Check SNAP installation
- Help configure your credentials

### 5. Configure Your Study Area and Credentials

Edit `02_config/parameters.yaml`:

**Study Area - Update WKT Geometry (That's ALL You Need!):**
```yaml
study_area:
  name: "Your Study Area Name"
  wkt_geometry: "POLYGON ((lon1 lat1, lon2 lat2, lon3 lat3, lon4 lat4, lon1 lat1))"
```

**Credentials:**
```yaml
download:
  copernicus_user: "your_email@example.com"
  copernicus_password: "your_password"
```

## ⚡ How Automatic Geometry Update Works

**Don't edit XML files manually!** The workflow automatically handles everything:

1. **You update the WKT** in `parameters.yaml`
2. **Workflow starts** and automatically calls `update_snap_geometry.py`
3. **Script extracts bounds** from your WKT polygon
4. **All SNAP XML files update** with correct geometry:
   - ✅ `resample_subset.xml` - Updated with WKT for subsetting
   - ✅ `mosaic.xml` - Updated with bounds (variables preserved!)
   - ✅ All other processing files - Automatically sync'd
5. **Processing runs** with correct study area

**Key Points:**
- Only change the `wkt_geometry` - everything else updates automatically!
- Coordinates must be in (longitude, latitude) order
- Polygon must be closed (first coordinate = last coordinate)
- Variables in mosaic.xml are ALWAYS preserved during updates
- See [SETUP_GUIDE.md](07_documentation/SETUP_GUIDE.md) for detailed examples and getting coordinates

### 6. Run Your First Processing
```bash
# The workflow will automatically update geometry!
python run_workflow.py --action full --start-date 2025-05-15 --end-date 2025-05-16

# Or run just the processing pipeline
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml
```

## 📁 Directory Structure

```
sentinel2-water-quality/
├── 01_scripts/              # Core processing scripts
│   ├── download.py          # Data download functionality
│   ├── process_pipeline.py  # SNAP processing pipeline
│   ├── plotting.py          # Visualization and plotting
│   └── utils.py             # Utility functions
├── 02_config/              # Configuration files
│   ├── parameters.yaml      # Main configuration
│   └── snap_graphs/         # SNAP processing graphs
├── 03_raw_data/            # Downloaded satellite data
├── 04_processed_data/      # Intermediate processing results
├── 05_final_products/      # Final water quality maps
│   ├── chl/                # Chlorophyll-a maps
│   ├── tsm/                # Total Suspended Matter maps
│   ├── cdom/               # CDOM maps
│   └── true_color/         # True color composites
├── 06_logs/                # Processing logs
├── 07_documentation/       # Additional documentation
├── requirements.txt        # Python dependencies
├── quick_setup.py          # Setup and validation script
├── validate_system.py      # System validation
└── run_workflow.py         # Main workflow script
```

## 📊 Processing Workflow

### Single-tile vs Multi-tile Processing

The workflow automatically detects your study area coverage and adapts:

#### 🟢 Single-Tile Coverage
When your study area falls within a single Sentinel-2 tile:
```
Processing: C2RCC → CDOM Calculation → Plotting
Benefits:
  - No mosaic processing (30-50% faster)
  - Saves ~30-50% disk space
  - Direct output to final products
```

#### 🟠 Multi-Tile Coverage
When your study area spans multiple Sentinel-2 tiles:
```
Processing: C2RCC → Mosaic → CDOM Calculation → Plotting
Benefits:
  - Seamless coverage across tiles
  - Single unified product per date
  - Automatic tile stitching
```

**The workflow automatically detects tile count and adapts!**

### Complete Processing Steps

1. **Step 1**: Resample & Subset - Resample to 10m, subset to study area
2. **Step 2**: Reproject - Reproject to WGS84 (EPSG:4326)
3. **Step 3**: True Color - Generate true color RGB composites
4. **Step 4**: C2RCC Processing - Atmospheric correction & water quality retrieval
5. **Step 5**: Mosaic (if needed) - Combine multiple tiles (single-tile skips this)
6. **Step 6**: CDOM Calculation - Calculate CDOM from atmospherically corrected data
7. **Step 7**: Visualization - Generate publication-ready plots

## 🔧 Usage

### Basic Commands

#### Full Workflow (Recommended)
```bash
# Download, process, and plot for specific dates
python run_workflow.py --action full --start-date 2025-05-15 --end-date 2025-05-16

# Use default dates from config
python run_workflow.py --action full
```

#### Using Individual Scripts (Direct Processing)
```bash
# Download data only
python 01_scripts/download.py --config 02_config/parameters.yaml

# Process data pipeline (full or individual steps)
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml

# Run individual processing steps (geometry updates automatically)
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 1  # Resample & Subset
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 2  # Reproject
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 3  # True Color
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 4  # C2RCC Processing
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 5  # Mosaic (if multi-tile)
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 6  # CDOM Calculation
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 7  # Generate Plots

# Generate plots only
python 01_scripts/plotting.py --config 02_config/parameters.yaml --parameter all   # All parameters
python 01_scripts/plotting.py --config 02_config/parameters.yaml --parameter chl   # Chlorophyll only
python 01_scripts/plotting.py --config 02_config/parameters.yaml --parameter tsm   # TSM only
python 01_scripts/plotting.py --config 02_config/parameters.yaml --parameter cdom  # CDOM only

# Update geometry manually (optional - automatic during processing)
python 01_scripts/update_snap_geometry.py --config 02_config/parameters.yaml
```

#### Individual Steps (Legacy)
```bash
# Download only
python run_workflow.py --action download --start-date 2025-05-15 --end-date 2025-05-16

# Process only (after download)
python run_workflow.py --action process

# Plot only (after processing)
python run_workflow.py --action plot
```

#### Utility Commands
```bash
# Clean processed data before new processing
python run_workflow.py --action full --clean

# Validate system setup
python validate_system.py

# Quick setup and configuration
python quick_setup.py
```

### Configuration

Edit `02_config/parameters.yaml` with your settings:

```yaml
# Study area and credentials
study_area:
  name: "Your Study Area"
  wkt_geometry: "POLYGON ((lon1 lat1, lon2 lat2, ...))"
  
download:
  copernicus_user: "your_email@example.com"
  copernicus_password: "your_password"
  cloud_cover_threshold: 10
  
# Processing parameters (use defaults or customize)
processing:
  target_resolution: 10
  target_crs: "EPSG:4326"
```

**For complete configuration options, see [WORKFLOW_DOCUMENTATION.md](07_documentation/WORKFLOW_DOCUMENTATION.md)**

## 🗺️ Study Area Configuration

The workflow is designed to be **study-area agnostic**. Simply configure your area once, and all processing updates automatically!

### Step 1: Define Your Study Area (WKT Polygon)

Edit `02_config/parameters.yaml`:

```yaml
study_area:
  name: "Your Study Area"
  wkt_geometry: "POLYGON ((lon1 lat1, lon2 lat2, lon3 lat3, lon4 lat4, lon1 lat1))"
  epsg_code: 4326
```

### Step 2: Get Coordinates

Use one of these methods:

**Option A: Online Tool (Recommended)**
- Visit [geojson.io](https://geojson.io/)
- Draw a polygon around your area
- Copy the coordinates and format as WKT

**Option B: QGIS**
1. Draw a rectangle/polygon
2. Right-click → Copy as WKT
3. Paste into parameters.yaml

**Option C: Manual**
- Get corner coordinates (longitude, latitude)
- Format: `POLYGON ((lon1 lat1, lon2 lat2, lon3 lat3, lon4 lat4, lon1 lat1))`

### Step 3: That's It!

The workflow will automatically:
- ✅ Extract geographic bounds
- ✅ Update all SNAP XML files
- ✅ Apply to resampling, subsetting, mosaicing
- ✅ Process your exact study area

**No manual XML editing needed!**

### Examples

**Western Australia Coast (Single-tile):**
```yaml
wkt_geometry: "POLYGON ((115.54 -31.93, 115.79 -31.93, 115.79 -32.26, 115.54 -32.26, 115.54 -31.93))"
```

**Great Barrier Reef (Multi-tile):**
```yaml
wkt_geometry: "POLYGON ((142.0 -10.0, 156.0 -10.0, 156.0 -24.0, 142.0 -24.0, 142.0 -10.0))"
```

For more examples, see [SETUP_GUIDE.md](07_documentation/SETUP_GUIDE.md)

## 📊 Outputs

The toolkit generates water quality maps and intermediate data products:

### Final Products (05_final_products/)

**Water Quality Maps** - Publication-ready PNG files:
- **Chlorophyll-a (CHL)**: `chl/` - Phytoplankton biomass
- **Total Suspended Matter (TSM)**: `tsm/` - Particulate matter concentration
- **Colored Dissolved Organic Matter (CDOM)**: `cdom/` - Dissolved organic compounds
- **True Color Composites**: `true_color/` - RGB visualization

All maps include:
- Cartographic projection (PlateCarree)
- Custom colormaps optimized for water quality visualization
- High resolution (300 DPI) suitable for publication
- Transparent backgrounds

### Intermediate Products (04_processed_data/)

**Processing Stages:**
- `l2a_resampled/` - Resampled to 10m resolution
- `l2a_reprojected/` - Reprojected to WGS84
- `c2rcc_output/` - C2RCC processed data (each tile individually)
- `mosaic_output/` - Mosaicked data (multi-tile only - created automatically if needed)
- `cdom_output/` - CDOM calculated products

**Automatic Source Selection:**
- ✅ CDOM calculated from **mosaic** (multi-tile) OR **C2RCC** (single-tile) - automatically selected
- ✅ Plotting reads from **both** C2RCC and mosaic_output as needed
- ✅ No manual intervention required - workflow adapts intelligently

### Raw Data (03_raw_data/)

- `sentinel2_l1c/` - Downloaded Sentinel-2 L1C ZIP files

### Logs (06_logs/)

- Processing logs with timestamps for debugging and quality control
- Each run creates separate log file: `processing_YYYYMMDD_HHMMSS.log`

## 🛠️ Troubleshooting

### Common Issues

#### SNAP Not Found
```bash
# Check SNAP installation
gpt -h
```
If SNAP is not found, verify installation and PATH configuration.

#### Python Package Errors
```bash
# Install missing packages
pip install -r requirements.txt
```

#### Download/Processing Errors
- Verify Copernicus credentials in `02_config/parameters.yaml`
- Check internet connection and available disk space
- Review log files in `06_logs/` for detailed error messages

### Getting Help

1. **Check Logs**: Review files in `06_logs/` for detailed error messages
2. **Run Diagnostics**: Use `python validate_system.py`
3. **Documentation**: See `07_documentation/` for comprehensive guides
4. **Issues**: Create an issue on GitHub for bugs or questions

## 📚 Scientific Background

### Water Quality Parameters
- **Chlorophyll-a (CHL)**: Phytoplankton biomass indicator
- **Total Suspended Matter (TSM)**: Particulate matter concentration
- **Colored Dissolved Organic Matter (CDOM)**: Dissolved organic compounds

### Processing Algorithm
Uses **C2RCC (Case 2 Regional CoastColour)** for atmospheric correction and water quality parameter retrieval from Sentinel-2 MSI data.

**For detailed technical information, see [WORKFLOW_DOCUMENTATION.md](07_documentation/WORKFLOW_DOCUMENTATION.md)**

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## �‍💻 Author

**Md Rony Golder**  
📧 [mdrony.golder@uwa.edu.au](mailto:mdrony.golder@uwa.edu.au)  
🏛️ University of Western Australia

## �🙏 Acknowledgments

- **ESA (European Space Agency)** for Sentinel-2 data
- **Copernicus Programme** for data access
- **SNAP Development Team** for processing tools
- **C2RCC Algorithm Developers** for water quality algorithms

## � Documentation

### Online Documentation
- **Read the Docs**: [https://sentinel2-water-quality.readthedocs.io/](https://sentinel2-water-quality.readthedocs.io/) (after setup)

### Local Documentation
You can build the documentation locally:

```bash
# Install documentation dependencies
pip install -r docs/requirements.txt

# Build HTML documentation
cd docs
make html

# Open in browser
start _build/html/index.html  # Windows
open _build/html/index.html   # macOS
xdg-open _build/html/index.html  # Linux
```

### Setup Read the Docs
1. Go to [https://readthedocs.org/](https://readthedocs.org/)
2. Sign up/Login with your GitHub account
3. Import your repository
4. The documentation will be automatically built from the `.readthedocs.yaml` configuration

## �📞 Support

- **Issues**: [Create an issue on GitHub](https://github.com/ronygolderku/sentinel2-water-quality/issues)
- **Documentation**: See `07_documentation/` folder or online docs
- **Troubleshooting**: Check logs in `06_logs/` and run `python validate_system.py`

---

© 2026 Md Rony Golder. All rights reserved.

**Happy Processing! 🛰️🌊**
