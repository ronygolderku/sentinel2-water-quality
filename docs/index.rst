================================================================================
Sentinel-2 Water Quality Processing Toolkit Documentation
================================================================================

A comprehensive, automated toolkit for processing Sentinel-2 satellite imagery to extract water quality parameters including Chlorophyll-a (CHL), Total Suspended Matter (TSM), and Colored Dissolved Organic Matter (CDOM).

.. image:: https://img.shields.io/badge/python-3.8%2B-blue
.. image:: https://img.shields.io/badge/license-MIT-green
.. image:: https://img.shields.io/badge/Sentinel--2-MSI-orange

**Key Features:**

- 🎯 Study-Area Agnostic - Update WKT geometry once, all SNAP XML files update automatically
- 🗺️ Intelligent Multi-tile Processing - Automatically detects and handles single vs multi-tile coverage
- ⚙️ Automated Data Download from Copernicus Data Space Ecosystem
- 🔄 Complete Processing Pipeline using SNAP and C2RCC algorithms
- 💧 Water Quality Parameter Extraction (CHL, TSM, CDOM)
- 📊 Automated Visualization with publication-ready plots
- 📁 Professional Directory Structure with organized outputs
- 🛡️ Comprehensive Error Handling and logging

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   getting_started
   setup_guide

.. toctree::
   :maxdepth: 2
   :caption: Usage & Workflow

   workflow_documentation
   features_summary

.. toctree::
   :maxdepth: 2
   :caption: Technical Guides

   snap_installation
   implementation_guide

.. toctree::
   :maxdepth: 2
   :caption: Support & Reference

   troubleshooting_guide
   api_reference

Quick Start
-----------

**1. Update Study Area**

Edit ``02_config/parameters.yaml``:

.. code-block:: yaml

    study_area:
      name: "Your Study Area"
      wkt_geometry: "POLYGON ((lon1 lat1, lon2 lat2, lon3 lat3, lon4 lat4, lon1 lat1))"

**2. Set Credentials**

.. code-block:: yaml

    download:
      copernicus_user: "your_email@example.com"
      copernicus_password: "your_password"

**3. Run Processing**

.. code-block:: bash

    python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml

That's it! The workflow automatically handles everything:

✅ Extracts geographic bounds from WKT
✅ Updates all SNAP XML files
✅ Downloads data for your study area
✅ Processes single or multiple tiles intelligently
✅ Generates publication-ready water quality maps

Main Features
--------------

**Automatic Study Area Configuration**

No manual XML editing required! The workflow automatically:

- Reads your WKT polygon from ``parameters.yaml``
- Extracts geographic bounds
- Updates all SNAP processing files
- Applies geometry consistently across all steps

**Multi-tile & Single-tile Handling**

The system intelligently adapts to your data:

- **Single-tile**: Skips mosaic, saves ~30-50% disk space
- **Multi-tile**: Automatically creates seamless mosaics
- **Adaptive processing**: CDOM and plotting adapt to available data

**Complete Water Quality Extraction**

Generate three key parameters from Sentinel-2:

- **Chlorophyll-a (CHL)**: Phytoplankton biomass indicator
- **Total Suspended Matter (TSM)**: Particulate concentration
- **Colored Dissolved Organic Matter (CDOM)**: Dissolved organics

Support & Documentation
------------------------

📖 **Documentation Files** in ``07_documentation/``:

- :doc:`setup_guide` - Detailed step-by-step setup
- :doc:`workflow_documentation` - Complete workflow reference
- :doc:`troubleshooting_guide` - Solutions to common issues
- :doc:`snap_installation` - SNAP installation guide

🐛 **Issues & Questions:**

- Review logs in ``06_logs/`` for debugging
- Run ``python validate_system.py`` for diagnostics
- Check tutorial files for examples

License
-------

This project is licensed under the MIT License. See the LICENSE file in the repository for details.

Author
------

**Md Rony Golder**

📧 mdrony.golder@uwa.edu.au

🏛️ University of Western Australia

Acknowledgments
---------------

- **ESA (European Space Agency)** for Sentinel-2 data
- **Copernicus Programme** for data access
- **SNAP Development Team** for processing tools
- **C2RCC Algorithm Developers** for water quality algorithms

---

**Happy Processing! 🛰️🌊**
