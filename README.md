# Sentinel-2 Water Quality Processing Toolkit

A comprehensive, automated toolkit for processing Sentinel-2 satellite imagery to extract water quality parameters including Chlorophyll-a (CHL), Total Suspended Matter (TSM), and Colored Dissolved Organic Matter (CDOM).

## 🌊 Features

- **Automated Data Download** from Copernicus Data Space Ecosystem
- **Complete Processing Pipeline** using SNAP and C2RCC algorithms
- **Water Quality Parameter Extraction** (CHL, TSM, CDOM)
- **Automated Visualization** with publication-ready plots
- **Professional Directory Structure** with organized outputs
- **Comprehensive Error Handling** and logging
- **Easy Configuration** via YAML files

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

### 5. Configure Your Credentials
Edit `02_config/parameters.yaml`:
```yaml
download:
  copernicus_user: "your_email@example.com"
  copernicus_password: "your_password"
```

### 6. Run Your First Processing
```bash
# Download, process, and plot data for a specific date range
python run_workflow.py --action full --start-date 2025-05-15 --end-date 2025-05-16
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

## 🔧 Usage

### Basic Commands

#### Full Workflow (Recommended)
```bash
# Download, process, and plot for specific dates
python run_workflow.py --action full --start-date 2025-05-15 --end-date 2025-05-16

# Use default dates from config
python run_workflow.py --action full
```

#### Individual Steps
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

Configure your study area in `02_config/parameters.yaml`:

```yaml
study_area:
  name: "Your Study Area"
  wkt_geometry: "POLYGON ((lon1 lat1, lon2 lat2, ...))"
  epsg_code: 4326
```

**Tip**: Use [geojson.io](https://geojson.io/) to draw polygons and get coordinates.

## 📊 Outputs

The toolkit generates several types of outputs:

### 1. Water Quality Maps
- **Chlorophyll-a (CHL)**: `05_final_products/chl/`
- **Total Suspended Matter (TSM)**: `05_final_products/tsm/`
- **Colored Dissolved Organic Matter (CDOM)**: `05_final_products/cdom/`

### 2. Visual Products
- **True Color Composites**: `05_final_products/true_color/`
- **PNG Maps**: Ready for publication or presentation

### 3. Data Products
- **NetCDF Files**: `04_processed_data/` (scientific data format)
- **Processing Logs**: `06_logs/` (detailed processing information)

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

© 2025 Md Rony Golder. All rights reserved.

**Happy Processing! 🛰️🌊**
