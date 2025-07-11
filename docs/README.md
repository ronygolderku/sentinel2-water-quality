# Documentation

This directory contains the Sphinx documentation source files for the Sentinel-2 Water Quality Processing Toolkit.

## Building Documentation Locally

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Build HTML documentation:
   ```bash
   make html
   ```

3. View documentation:
   ```bash
   # Windows
   start _build/html/index.html
   
   # macOS
   open _build/html/index.html
   
   # Linux
   xdg-open _build/html/index.html
   ```

## Online Documentation

The documentation is automatically built and deployed to:
- **Read the Docs**: https://sentinel2-water-quality.readthedocs.io/

## Files

- `conf.py` - Sphinx configuration
- `index.md` - Main documentation index
- `*.md` - Documentation pages (copied from `../07_documentation/`)
- `Makefile` - Build commands for Unix/Linux/macOS
- `make.bat` - Build commands for Windows
- `requirements.txt` - Python packages needed for building docs
