# Getting Started Guide

Welcome to the Sentinel-2 Water Quality Processing Toolkit! This guide provides detailed setup instructions beyond the Quick Start in the main README.

**Before You Start**: If you're new to water quality remote sensing or want to understand the science behind this toolkit, we recommend reading [Scientific Background & Theory](scientific_background.md) first. It covers:
- Why water quality monitoring matters
- How Sentinel-2 satellites work
- The C2RCC atmospheric correction algorithm
- What the water quality parameters mean
- Why single vs multi-tile processing matters

## Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher
- At least 8GB RAM (16GB recommended)
- 10GB+ free disk space
- Internet connection
- Git installed

## Detailed Setup Instructions

### 1. Repository Setup
```bash
git clone https://github.com/ronygolderku/sentinel2-water-quality.git
cd sentinel2-water-quality
```

### 2. Python Environment
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. SNAP Installation

**For detailed SNAP installation instructions, see [SNAP_INSTALLATION_GUIDE.md](SNAP_INSTALLATION_GUIDE.md)**

Quick verification:
```bash
# Test SNAP installation
gpt -h
```

If SNAP is not found, follow the comprehensive installation guide in the documentation folder.

### 4. Copernicus Account Setup
1. Go to [https://identity.dataspace.copernicus.eu/](https://identity.dataspace.copernicus.eu/)
2. Click "Register" and create a free account
3. Verify your email address
4. Note your username and password

### 6. Configure the Toolkit
```bash
# Run the quick setup
python quick_setup.py

# Or manually configure
cp 02_config/parameters_template.yaml 02_config/parameters.yaml
# Edit parameters.yaml with your credentials and study area
```

### 7. Define Your Study Area
Update the study area in `02_config/parameters.yaml`:

```yaml
study_area:
  name: "My Study Area"
  wkt_geometry: "POLYGON ((your coordinates here))"
  epsg_code: 4326
```

**Tips for defining your study area:**
- Use [geojson.io](https://geojson.io/) to draw your polygon
- Keep the area reasonable (< 100km²) for faster processing
- Ensure coordinates are in WGS84 (EPSG:4326)

### 8. Test Your Setup
```bash
# Validate your installation
python validate_system.py

# Should show all green checkmarks ✅
```

### 9. Run Your First Processing
```bash
# Process a small date range first
python run_workflow.py --action full --start-date 2025-05-15 --end-date 2025-05-16
```

## Common Commands

### Download Data Only
```bash
python run_workflow.py --action download --start-date 2025-05-15 --end-date 2025-05-16
```

### Process Downloaded Data
```bash
python run_workflow.py --action process
```

### Generate Plots Only
```bash
python run_workflow.py --action plot
```

### Full Workflow
```bash
python run_workflow.py --action full --start-date 2025-05-15 --end-date 2025-05-16
```

### Clean and Restart
```bash
python run_workflow.py --action full --clean --start-date 2025-05-15 --end-date 2025-05-16
```

## Expected Processing Time

### Single-Tile Processing
- **Download**: 2-10 minutes per scene
- **Processing**: 5-15 minutes per scene (no mosaic required)
- **Plotting**: 1-5 minutes per scene
- **Total**: ~30% faster than multi-tile

**Disk Space**: ~2-3GB per scene

### Multi-Tile Processing
- **Download**: 5-20 minutes per date (multiple tiles)
- **Processing**: 10-30 minutes per date (includes mosaic)
- **Plotting**: 1-5 minutes per date

**Disk Space**: ~3-5GB per date (more tiles = more space)

### Automatic Detection
The workflow **automatically detects** whether your study area needs:
- ✅ **Single-tile processing** (faster, less disk space)
- ✅ **Multi-tile processing** (seamless coverage, automatic mosaicing)

No configuration needed - it just works!

*Times depend on your internet speed, system performance, and scene size.*

## Output Files

After successful processing, you'll find:

```
05_final_products/
├── chl/           # Chlorophyll-a maps
├── tsm/           # Total Suspended Matter maps
├── cdom/          # CDOM maps
└── true_color/    # True color composites
```

## Troubleshooting

### SNAP Not Found
```bash
# Check if SNAP is in PATH
gpt -h

# If not found, add SNAP to PATH or reinstall
```

### Python Package Issues
```bash
# Update pip and retry
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Download Issues
- Check Copernicus credentials
- Verify internet connection
- Ensure study area coordinates are valid

### Processing Errors
- Check available disk space
- Review log files in `06_logs/`
- Ensure SNAP is properly installed

## Getting Help

1. **Check the logs**: Look in `06_logs/` for detailed error messages
2. **Run diagnostics**: Use `python validate_system.py`
3. **Quick setup**: Run `python quick_setup.py` for guided troubleshooting
4. **GitHub Issues**: Report bugs or ask questions on GitHub

## Next Steps

Once you have the toolkit working:

1. **Experiment with different study areas**
2. **Try different date ranges**
3. **Customize processing parameters**
4. **Integrate with your research workflow**

Happy processing! 🛰️🌊
