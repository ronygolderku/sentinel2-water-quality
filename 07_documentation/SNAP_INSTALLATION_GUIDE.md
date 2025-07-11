# SNAP Installation Guide for Sentinel-2 Water Quality Processing

## What is SNAP?

SNAP (Sentinel Application Platform) is ESA's official toolbox for processing Sentinel satellite data. It's required for:
- Atmospheric correction (C2RCC)
- Geometric correction
- Radiometric calibration
- Band math operations

## Installation Steps

### 1. Download SNAP

1. Visit: https://step.esa.int/main/download/snap-download/
2. Click "Download SNAP 10.0" (or latest version)
3. Choose your operating system (Windows/Linux/Mac)
4. Download the installer (approximately 1.5 GB)

### 2. Install SNAP

1. **Run the installer as Administrator**
2. **Accept the license agreement**
3. **Choose installation directory** (default is fine: `C:\Program Files\snap`)
4. **Select components to install:**
   - ✅ SNAP Desktop
   - ✅ Sentinel-1 Toolbox
   - ✅ Sentinel-2 Toolbox  
   - ✅ Sentinel-3 Toolbox
   - ✅ SNAP GPT (Graph Processing Tool) - **REQUIRED**
5. **Install** (this may take 15-30 minutes)

### 3. Verify Installation

Open Command Prompt and test:
```bash
# Test GPT command
gpt --help

# If you see help text, SNAP is working!
```

### 4. Add SNAP to PATH (if needed)

If `gpt --help` doesn't work, add SNAP to your system PATH:

#### Windows:
1. **Open System Properties:**
   - Right-click "This PC" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"

2. **Edit PATH:**
   - In "System variables", find "Path"
   - Click "Edit"
   - Click "New"
   - Add: `C:\Program Files\snap\bin`
   - Click "OK" on all windows

3. **Restart Command Prompt** and test: `gpt --help`

### 5. Configure SNAP (Optional)

For better performance, you can increase SNAP's memory allocation:

1. **Find SNAP configuration:**
   - Windows: `C:\Program Files\snap\bin\gpt.vmoptions`

2. **Edit the file** (as Administrator):
   ```
   -Xmx8G
   -Xms1G
   -XX:+UseG1GC
   ```
   (Adjust `-Xmx8G` to your available RAM, e.g., `-Xmx4G` for 4GB)

## Troubleshooting

### Common Issues

1. **"gpt is not recognized"**
   - SNAP is not in PATH
   - Solution: Add `C:\Program Files\snap\bin` to PATH

2. **"Java heap space" errors**
   - Insufficient memory allocated
   - Solution: Increase `-Xmx` value in `gpt.vmoptions`

3. **Installation fails**
   - Run installer as Administrator
   - Temporarily disable antivirus
   - Ensure sufficient disk space (>5GB)

4. **SNAP Desktop won't start**
   - Check Java version (SNAP requires Java 8+)
   - Update graphics drivers

### Testing SNAP Installation

Run these commands to verify SNAP is working:

```bash
# Basic help
gpt --help

# List available operators
gpt -h

# Test C2RCC operator (required for water quality)
gpt c2rcc.msi -h
```

## Integration with Water Quality Workflow

Once SNAP is installed, your workflow will use these SNAP operators:

1. **Read** - Load Sentinel-2 data
2. **Resample** - Resample bands to 10m
3. **Subset** - Extract study area
4. **Reproject** - Convert to WGS84
5. **C2RCC** - Atmospheric correction for water
6. **BandMaths** - Calculate CDOM
7. **Write** - Save results

## Performance Tips

1. **Increase Java heap size:** `-Xmx8G` or higher
2. **Use SSD storage** for faster I/O
3. **Close other applications** during processing
4. **Process smaller areas** if memory is limited

## Alternative: Docker Installation

If you have issues with the regular installation, you can use SNAP in Docker:

```bash
# Pull SNAP Docker image
docker pull mundialis/esa-snap:latest

# Run SNAP GPT
docker run -v /path/to/data:/data mundialis/esa-snap gpt --help
```

## Getting Help

- **SNAP Forum:** https://forum.step.esa.int/
- **SNAP Documentation:** https://step.esa.int/main/doc/
- **Tutorials:** https://step.esa.int/main/doc/tutorials/

## Quick Start After Installation

1. **Verify installation:** `gpt --help`
2. **Run system validation:** `python validate_system.py`
3. **Update credentials:** Edit `02_config/parameters.yaml`
4. **Run workflow:** `run_workflow.bat`

## System Requirements

- **OS:** Windows 10/11, Linux, macOS
- **RAM:** 8GB minimum, 16GB recommended
- **Disk:** 10GB for installation, 50GB+ for processing
- **Java:** Version 8 or higher (usually included with SNAP)

Remember: SNAP installation is a one-time setup. Once installed and configured, your water quality processing workflow will run automatically!
