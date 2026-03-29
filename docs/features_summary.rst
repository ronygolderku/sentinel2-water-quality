Features Summary
================

Key Capabilities
----------------

Study-Area Agnostic Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Update Only One Place:** Your WKT polygon in ``parameters.yaml``

The workflow automatically:

✅ Extracts geographic bounds from WKT
✅ Updates all SNAP processing XML files
✅ Applies geometry to resampling, subsetting, mosaicing
✅ No manual XML editing required
✅ Works for any geographic location on Earth

**Example:**

.. code-block:: yaml

    study_area:
      wkt_geometry: "POLYGON ((115.54 -31.93, 115.79 -31.93, 115.79 -32.26, 115.54 -32.26, 115.54 -31.93))"

That's all! Everything updates automatically.

Intelligent Multi-tile Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Automatic Detection:** The system analyzes Sentinel-2 tile coverage for your area

**Single-tile Areas:**

- ✅ Skips mosaic processing
- ✅ Saves ~30-50% disk space
- ✅ Processes 30-50% faster
- ✅ Direct output to final products

**Multi-tile Areas:**

- ✅ Automatically creates mosaics
- ✅ Seamless coverage across tiles
- ✅ Single unified product per date
- ✅ Transparent to user

**No Configuration Needed!** The system detects and adapts automatically.

Complete Water Quality Extraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract three key water quality parameters from Sentinel-2:

1. **Chlorophyll-a (CHL)** - Phytoplankton biomass
2. **Total Suspended Matter (TSM)** - Particle concentration  
3. **Colored Dissolved Organic Matter (CDOM)** - Dissolved organics

All computed using the C2RCC atmospheric correction algorithm.

Automated Data Download
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    python 01_scripts/download.py --config 02_config/parameters.yaml

- ✅ Connects to Copernicus Data Space Ecosystem
- ✅ Filters by date range
- ✅ Filters by cloud cover threshold
- ✅ Downloads only Sentinel-2 L1C data for your area
- ✅ Automatic retry and error recovery

Complete Processing Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

7-step automated pipeline:

1. Resample & Subset
2. Reproject to WGS84
3. True Color Generation
4. C2RCC Atmospheric Correction
5. Multi-tile Mosaic (if needed)
6. CDOM Calculation
7. Publication-Ready Visualization

**Single Command:**

.. code-block:: bash

    python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml

Or run individual steps:

.. code-block:: bash

    python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 1

Adaptive Visualization
~~~~~~~~~~~~~~~~~~~~~~

- ✅ Reads from both C2RCC and mosaic outputs
- ✅ Generates plots automatically
- ✅ Works seamlessly for single or multi-tile scenarios
- ✅ Publication-ready PNG outputs (300 DPI)
- ✅ Custom colormaps optimized for water quality

Professional Directory Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Organized, easy-to-navigate output:

.. code-block:: text

    03_raw_data/sentinel2_l1c/      - Downloaded data
    04_processed_data/              - Intermediate products
    05_final_products/              
        ├── chl/                    - Chlorophyll maps
        ├── tsm/                    - TSM maps
        ├── cdom/                   - CDOM maps
        └── true_color/             - RGB composites
    06_logs/                        - Processing logs
    07_documentation/               - Documentation

Comprehensive Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ✅ Gracefully handles missing data
- ✅ No manual intervention required
- ✅ Detailed logging all steps
- ✅ Log files with timestamps
- ✅ Clear error messages

Logging
~~~~~~~

Every run creates a log file in ``06_logs/``:

.. code-block:: text

    processing_YYYYMMDD_HHMMSS.log

Contains:

- ✅ Step-by-step progress
- ✅ File processing details
- ✅ Error messages (if any)
- ✅ Processing duration
- ✅ File counts and statistics

Performance Features
~~~~~~~~~~~~~~~~~~~

- ✅ Single-tile spatial optimization (30-50% faster)
- ✅ Disk space optimization (30-50% less space)
- ✅ Cached processed data avoids recomputation
- ✅ Parallel processing support via SNAP
- ✅ Memory-efficient processing

Cross-Platform Support
~~~~~~~~~~~~~~~~~~~~~

Works on:

- ✅ Windows 10/11
- ✅ Linux (Ubuntu, Debian, etc.)
- ✅ macOS

Same codebase, no platform-specific configuration needed.
