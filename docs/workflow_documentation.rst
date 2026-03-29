Workflow Documentation
======================

Complete Processing Pipeline
-----------------------------

The workflow consists of 7 automated steps:

1. **Resample & Subset** - Resample bands to 10m, subset to study area
2. **Reproject** - Project to WGS84 (EPSG:4326)
3. **True Color** - Generate RGB composites
4. **C2RCC Processing** - Atmospheric correction & water quality retrieval
5. **Mosaic (Conditional)** - Combine multiple tiles (if needed)
6. **CDOM Calculation** - Calculate CDOM parameter
7. **Visualization** - Generate publication-ready plots

Step Details
~~~~~~~~~~~~

**Step 1: Resample & Subset**

- Resamples all bands to 10m resolution using Band 2 as reference
- Subsets data to your study area (WKT polygon)
- Output: BEAM-DIMAP format in ``l2a_resampled/``

**Step 2: Reproject**

- Reprojects to WGS84 coordinate system
- Maintains spatial resolution and extent
- Output: BEAM-DIMAP format in ``l2a_reprojected/``

**Step 3: True Color**

- Generates RGB true color images
- Uses Band 4 (Red), Band 3 (Green), Band 2 (Blue)
- Output: PNG images in ``true_color/``

**Step 4: C2RCC Processing**

- Applies Case 2 Regional Coast Color atmospheric correction
- Calculates CHL and TSM parameters
- Processes each tile individually
- Output: NetCDF files in ``c2rcc_output/``

**Step 5: Mosaic (Conditional)**

- **Single-tile**: Skipped automatically (saves time & space)
- **Multi-tile**: Automatically creates seamless mosaic
- Output: NetCDF files in ``mosaic_output/``

**Step 6: CDOM Calculation**

- Calculates CDOM using band math
- Uses mosaic if available, otherwise C2RCC data
- Output: NetCDF files in ``cdom_output/``

**Step 7: Visualization**

- Generates plots for CHL, TSM, CDOM
- Reads from both C2RCC and mosaic sources (adaptive)
- Output: PNG plots in ``05_final_products/``

Single vs Multi-tile Workflow
-----------------------------

The system automatically detects and adapts to your coverage:

**Single-Tile Scenario**

When your study area falls in one Sentinel-2 tile:

.. code-block:: text

    Workflow: C2RCC → CDOM → Plotting
    Benefits:
      - No mosaic processing (30-50% faster)
      - Saves ~30-50% disk space
      - Direct output to final products

**Multi-Tile Scenario**

When your study area spans multiple Sentinel-2 tiles:

.. code-block:: text

    Workflow: C2RCC → Mosaic → CDOM → Plotting
    Benefits:
      - Seamless coverage across tiles
      - Single unified product per date
      - Automatic tile stitching

Automatic Detection
~~~~~~~~~~~~~~~~~~~

The workflow automatically:

1. Groups C2RCC outputs by date
2. Counts tiles per date
3. For single-tile: Skips mosaic, processes directly
4. For multi-tile: Creates mosaic, then processes
5. CDOM adapts to available source
6. Plotting reads from both directories

Data Outputs
------------

**Final Products (05_final_products/)**

.. code-block:: text

    chl/           - Chlorophyll-a maps (PNG, 300 DPI)
    tsm/           - Total Suspended Matter maps (PNG, 300 DPI)
    cdom/          - CDOM maps (PNG, 300 DPI)
    true_color/    - True color RGB composites (PNG)

**Intermediate Data (04_processed_data/)**

.. code-block:: text

    l2a_resampled/      - Resampled data
    l2a_reprojected/    - Reprojected data
    c2rcc_output/       - Per-tile C2RCC products
    mosaic_output/      - Multi-tile mosaics (if created)
    cdom_output/        - CDOM calculations

**Raw Data (03_raw_data/)**

.. code-block:: text

    sentinel2_l1c/      - Downloaded Sentinel-2 ZIP files

Water Quality Parameters
------------------------

**Chlorophyll-a (CHL)**

- Units: mg/m³
- Range: 0.01 - 20.0 mg/m³
- Indicator: Phytoplankton biomass
- Colormap: Custom 21-color scale

**Total Suspended Matter (TSM)**

- Units: g/m³
- Range: 0 - 4 g/m³
- Indicator: Particulate concentration
- Colormap: CMOcean turbid

**Colored Dissolved Organic Matter (CDOM)**

- Units: m⁻¹
- Range: 0 - 4 m⁻¹
- Indicator: Dissolved organics
- Colormap: YlOrBr

Algorithm
---------

Uses **C2RCC (Case 2 Regional CoastColour)** algorithm:

.. code-block:: text

    CDOM = exp(0.544 * log(rhown_B1) - 0.571 * log(rhown_B2) 
           - 2.181 * log(rhown_B3) + 1.398 * log(rhown_B4) - 1.406)

Where rhown_Bi are water-leaving reflectances from C2RCC.

Regional Parameters (Australian Coastal Waters)

.. code-block:: yaml

    salinity: 35.0 psu
    temperature: 30.0°C
    tsm_factor: 1.06
    chl_factor: 21.0
