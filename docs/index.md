# Sentinel-2 Water Quality Processing Toolkit

```{toctree}
:maxdepth: 2
:caption: Contents:

getting_started
scientific_background
workflow_documentation
troubleshooting
snap_installation
api_reference
```

## Overview

A comprehensive, automated toolkit for processing Sentinel-2 satellite imagery to extract water quality parameters including Chlorophyll-a (CHL), Total Suspended Matter (TSM), and Colored Dissolved Organic Matter (CDOM).

## Features

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

## Scientific Foundation

This toolkit processes **Level-1C Sentinel-2 satellite imagery** to extract essential water quality indicators:

- 🔬 **Chlorophyll-a (Chl-a)**: Phytoplankton biomass & primary productivity
- 🌊 **Total Suspended Matter (TSM)**: Water turbidity & particulate load
- 🟫 **Colored Dissolved Organic Matter (CDOM)**: Dissolved organic compounds

Using the state-of-the-art **C2RCC (Case-2 Regional Coast Colour)** atmospheric correction algorithm, specifically designed for optically complex coastal and inland waters. The system automatically handles:
- Atmospheric correction
- Bio-optical parameter inversion
- Quality control and validation
- Single/multi-tile processing with automatic mosaic generation

**New to water quality remote sensing?** Start with [Scientific Background & Theory](scientific_background.md) to understand the science behind the toolkit.

## Quick Links

- [Getting Started](getting_started.md)
- [Scientific Background & Theory](scientific_background.md)
- [Workflow Documentation](workflow_documentation.md)
- [Troubleshooting Guide](troubleshooting.md)
- [API Reference](api_reference.md)

## Author

**Md Rony Golder**  
📧 [mdrony.golder@uwa.edu.au](mailto:mdrony.golder@uwa.edu.au)  
🏛️ University of Western Australia

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`

---

© 2025 Md Rony Golder. All rights reserved.
