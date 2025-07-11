# Troubleshooting Guide - Sentinel-2 Water Quality Processing

## Common Errors and Solutions

### 1. "Workflow completed with errors!"

This generic error message means something went wrong during processing. Here's how to diagnose:

#### Step 1: Check the Log Files
```bash
# Look at the newest log file in 06_logs/
dir 06_logs\ /o-d
# Open the most recent log file to see detailed error messages
```

#### Step 2: Run System Validation
```bash
python validate_system.py
```

### 2. Python Import Errors

**Error:** `ModuleNotFoundError: No module named 'yaml'` (or other packages)

**Solution:**
```bash
# Install missing packages
pip install -r requirements.txt

# Or install specific packages
pip install pyyaml pandas geopandas xarray matplotlib cartopy cmocean
```

### 3. SNAP GPT Not Found

**Error:** `'gpt' is not recognized as an internal or external command`

**Solution:**
1. Install SNAP from: https://step.esa.int/main/download/snap-download/
2. Add SNAP to your PATH environment variable:
   - Windows: Add `C:\Program Files\snap\bin` to PATH
   - Or restart command prompt after SNAP installation

### 4. Authentication Errors

**Error:** `Failed to get authentication token` or `401 Unauthorized`

**Solution:**
1. Update your Copernicus credentials in `02_config/parameters.yaml`:
   ```yaml
   download:
     copernicus_user: "your_actual_email@example.com"
     copernicus_password: "your_actual_password"
   ```

2. Verify credentials at: https://identity.dataspace.copernicus.eu/

### 5. Network/Download Errors

**Error:** `Connection timeout` or `No data found`

**Solution:**
1. Check internet connection
2. Verify date range - ensure data exists for your dates
3. Check cloud cover threshold (may be too restrictive)
4. Try smaller date ranges

### 6. Processing Errors

**Error:** `GPT processing failed` or `Java heap space`

**Solution:**
1. Increase Java heap size for SNAP:
   ```bash
   # Edit SNAP configuration
   # Windows: C:\Program Files\snap\bin\gpt.vmoptions
   # Add or modify: -Xmx8G (for 8GB RAM)
   ```

2. Ensure sufficient disk space (>10GB free)

### 7. File Permission Errors

**Error:** `Permission denied` or `Access denied`

**Solution:**
1. Run as Administrator
2. Check file permissions in processing directories
3. Ensure antivirus is not blocking file operations

### 8. Configuration Errors

**Error:** `Configuration file not found` or `KeyError`

**Solution:**
1. Ensure `02_config/parameters.yaml` exists
2. Check YAML syntax (indentation matters)
3. Verify all required fields are present

### 9. Memory Errors

**Error:** `Out of memory` or `Memory allocation error`

**Solution:**
1. Close other applications
2. Increase virtual memory/swap space
3. Process smaller areas or fewer dates at once
4. Increase Java heap size for SNAP

### 10. Path Errors

**Error:** `File not found` or `Path does not exist`

**Solution:**
1. Use forward slashes or double backslashes in paths
2. Ensure all directories exist
3. Check for special characters in paths

## Diagnostic Commands

### Check System Status
```bash
# Run complete validation
python validate_system.py

# Check specific components
python 01_scripts/utils.py --action validate --path .

# View processing statistics
python 01_scripts/utils.py --action stats --path .
```

### Check Individual Components
```bash
# Test Python packages
python -c "import yaml, pandas, xarray, matplotlib; print('Packages OK')"

# Test SNAP GPT
gpt --help

# Test configuration
python -c "import yaml; yaml.safe_load(open('02_config/parameters.yaml'))"
```

## Recovery Procedures

### Clean and Restart
```bash
# Clean processed data
python 01_scripts/utils.py --action clean --path .

# Restart processing
python run_workflow.py --action process --clean
```

### Step-by-Step Processing
```bash
# Run individual steps to isolate issues
python run_workflow.py --action download
python run_workflow.py --action process  
python run_workflow.py --action plot
```

## Getting Help

1. **Check Log Files:** Always check the newest log file in `06_logs/`
2. **Run Validation:** Use `python validate_system.py`
3. **Check Documentation:** Review `07_documentation/WORKFLOW_DOCUMENTATION.md`
4. **System Information:** Include OS, Python version, and error messages when seeking help

## Performance Tips

1. **Optimize Java Heap:** Set `-Xmx8G` or higher for SNAP
2. **Use SSD Storage:** Process on SSD for faster I/O
3. **Sufficient RAM:** 16GB+ recommended for large areas
4. **Network Stability:** Stable internet for downloads
5. **Close Applications:** Free up system resources

## Error Code Reference

- **Exit Code 0:** Success
- **Exit Code 1:** General error
- **Exit Code 2:** Invalid arguments
- **Exit Code 3:** File not found
- **Exit Code 4:** Permission denied
- **Exit Code 5:** Network error

Remember: Most errors are related to missing dependencies, incorrect configuration, or insufficient resources. The system validation script will help identify most issues quickly.
