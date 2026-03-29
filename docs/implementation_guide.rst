Implementation Guide
====================

Architecture Overview
---------------------

The system follows a modular architecture with clear separation of concerns:

.. code-block:: text

    Configuration (parameters.yaml)
           ↓
    Geometry Management (update_snap_geometry.py)
           ↓
    Data Download (download.py)
           ↓
    Processing Pipeline (process_pipeline.py)
           ├→ Resample & Subset
           ├→ Reproject
           ├→ True Color
           ├→ C2RCC
           ├→ Mosaic (Conditional)
           ├→ CDOM Calculation
           ↓
    Visualization (plotting.py)
           ↓
    Final Products

Automatic Geometry Configuration
--------------------------------

**How It Works:**

1. **User Action:** Update WKT in ``parameters.yaml``
2. **Processor Init:** ``update_snap_geometry()`` called
3. **Extraction:** Bounds extracted from WKT polygon
4. **Update:** All XML files updated with new bounds
5. **Processing:** Pipeline runs with correct geometry

**Safe Updates:**

- Regex patterns: Match only values in tags
- Variables preserved: Never removes XML variables
- Safe to run multiple times: No accumulation of changes

**Key Regex Patterns:**

.. code-block:: python

    # Resample_subset.xml
    r'<geoRegion>POLYGON\s*\(\s*\([^)]*\)\s*\)</geoRegion>'
    
    # Mosaic.xml
    r'<westBound>[^<]*</westBound>'
    r'<eastBound>[^<]*</eastBound>'
    r'<northBound>[^<]*</northBound>'
    r'<southBound>[^<]*</southBound>'

Multi-tile Detection & Processing
----------------------------------

**Detection Logic:**

.. code-block:: python

    def get_tiles_by_date(self):
        # 1. Read all C2RCC files
        # 2. Extract date from each filename
        # 3. Group by date
        # 4. Count tiles per date
        # 5. Return: {'date': {'single': [...], 'multiple': [...]}}

**Tile ID Extraction:**

Sentinel-2 filenames contain tile IDs like ``T52LFL``:

.. code-block:: text

    S2A_MSIL1C_20150903T014036_N0500_R031_T52LFL_20231017T130149.zip
                                                 ^^^^^^
```
    Pattern: ``T`` + 5 characters (e.g., T52LFL, T52LFM)

**Mosaic Decision:**

.. code-block:: python

    if num_tiles_for_date == 1:
        skip_mosaic()  # Saves 30-50% time and space
    elif num_tiles_for_date > 1:
        create_mosaic()  # Combines tiles
    
**Processing Flow:**

**Single-tile:**
- C2RCC → CDOM → Plotting

**Multi-tile:**
- C2RCC → Mosaic → CDOM → Plotting

**Both sources in parallel processing:**
- Plotting reads from both c2rcc_output and mosaic_output

Adaptive Source Selection
-------------------------

**CDOM Calculation:**

.. code-block:: python

    if mosaic_exists_for_date:
        use_mosaic_as_input()
    elif c2rcc_exists_for_date:
        use_c2rcc_as_input()
    else:
        skip_this_date()

**Plotting:**

.. code-block:: python

    # Check both directories
    mosaic_files = glob(mosaic_output/*.nc)
    c2rcc_files = glob(c2rcc_output/*.nc)
    
    # Process all available files
    plot(mosaic_files)
    plot(c2rcc_files)

Error Handling Strategy
-----------------------

**Graceful Degradation:**

- Missing data doesn't stop pipeline
- Returns ``True`` for non-critical failures
- Logs detailed error context
- Continues with next date/tile

**Examples:**

.. code-block:: python

    # No mosaic files = not an error
    if not mosaic_files:
        logger.info("Skipping mosaic step")
        return True
    
    # No C2RCC files = not an error
    if not c2rcc_files:
        logger.info("No files for CDOM")
        return True

**Error Logging:**

- Each step has try-except
- All errors logged with context
- Failed files listed with details
- Processing continues with remaining data

Performance Optimizations
-------------------------

**Single-tile Optimization:**

- Skips mosaic (saves 30-50% time)
- Skips mosaic bounds checking
- Direct C2RCC to CDOM
- Typical speedup: 2-3x for single-tile areas

**Disk Space Optimization:**

- No mosaic files for single-tile (saves ~30-50% space)
- Mosaic only created when needed
- Intermediate files can be cleaned

**Parallel SNAP Processing:**

- SNAP uses available CPU cores
- Multiple bands processed in parallel
- Mosaic uses multi-core stitching

Data Flow
---------

**Input:**

1. Sentinel-2 L1C ZIP files (downloaded)
2. Study area WKT geometry
3. Processing parameters

**Transformations:**

1. Resample: Individual bands → 10m resolution
2. Subset: Full scene → Study area extent
3. Reproject: Native CRS → WGS84
4. C2RCC: TOA reflectance → Water parameters
5. Mosaic: Individual tiles → Seamless coverage (if needed)
6. CDOM: Band math → CDOM parameter
7. Plotting: NetCDF → PNG visualization

**Output:**

1. Water quality maps (CHL, TSM, CDOM)
2. True color composites
3. NetCDF intermediate products
4. Processing logs

Configuration Precedence
------------------------

1. **Command line arguments** (highest)
2. **parameters.yaml**
3. **Defaults in code** (lowest)

Example:

.. code-block:: bash

    # Override config file dates
    python download.py --config ... \
      --start-date 2025-06-01 \
      --end-date 2025-06-30

Extension Points
----------------

**Custom Processing:**

Extend ``WaterQualityProcessor`` class:

.. code-block:: python

    class CustomProcessor(WaterQualityProcessor):
        def step_8_custom_analysis(self):
            # Add your processing here
            pass

**Custom Visualization:**

Extend ``WaterQualityPlotter`` class:

.. code-block:: python

    class CustomPlotter(WaterQualityPlotter):
        def plot_custom_parameter(self):
            # Add your plotting here
            pass

Debugging
---------

**Enable Verbose Logging:**

Set in ``parameters.yaml``:

.. code-block:: yaml

    logging:
      level: "DEBUG"

**Check Intermediate Files:**

.. code-block:: bash

    # After each step, check outputs
    ls -la 04_processed_data/l2a_resampled/
    ls -la 04_processed_data/l2a_reprojected/
    ls -la 04_processed_data/c2rcc_output/
    ls -la 04_processed_data/mosaic_output/
    ls -la 04_processed_data/cdom_output/

**Profile Performance:**

Add timing in logs:

.. code-block:: bash

    # Compare log timestamps
    grep "STEP.*Processing" 06_logs/processing_*.log | head -20

Testing
-------

**Unit Tests:**

- Geometry extraction functions
- Tile detection logic
- Date extraction

**Integration Tests:**

- Full pipeline on small area
- Multi-tile processing
- Error handling

**Manual Testing:**

1. Single-tile area → Verify no mosaic
2. Multi-tile area → Verify mosaic created
3. Small area → Full pipeline
4. Geometry update → Verify XML changes

Maintenance
-----------

**Update SNAP XML:**

After parameter changes:

.. code-block:: bash

    python update_snap_geometry.py --config 02_config/parameters.yaml

**Clean Old Data:**

.. code-block:: bash

    # Keep only latest, remove old processing
    rm -rf 04_processed_data/*
    rm -rf 06_logs/*

**Update Dependencies:**

.. code-block:: bash

    pip install --upgrade -r requirements.txt
