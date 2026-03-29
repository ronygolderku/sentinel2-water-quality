API Reference
=============

Command Line Interface
----------------------

Processing Pipeline
~~~~~~~~~~~~~~~~~~~

**Full Pipeline**

.. code-block:: bash

    python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml

**Individual Steps**

.. code-block:: bash

    # Step 1: Resample and Subset
    python 01_scripts/process_pipeline.py --config ... --step 1
    
    # Step 2: Reproject
    python 01_scripts/process_pipeline.py --config ... --step 2
    
    # Step 3: True Color
    python 01_scripts/process_pipeline.py --config ... --step 3
    
    # Step 4: C2RCC Processing
    python 01_scripts/process_pipeline.py --config ... --step 4
    
    # Step 5: Mosaic (if multi-tile)
    python 01_scripts/process_pipeline.py --config ... --step 5
    
    # Step 6: CDOM Calculation
    python 01_scripts/process_pipeline.py --config ... --step 6
    
    # Step 7: Generate Plots
    python 01_scripts/process_pipeline.py --config ... --step 7

Data Download
~~~~~~~~~~~~~

.. code-block:: bash

    python 01_scripts/download.py --config 02_config/parameters.yaml
    
    # With date range override
    python 01_scripts/download.py --config ... \
      --start-date 2025-05-01 --end-date 2025-05-31

Plotting
~~~~~~~~

.. code-block:: bash

    # All parameters
    python 01_scripts/plotting.py --config 02_config/parameters.yaml --parameter all
    
    # Specific parameter
    python 01_scripts/plotting.py --config ... --parameter chl
    python 01_scripts/plotting.py --config ... --parameter tsm
    python 01_scripts/plotting.py --config ... --parameter cdom

Geometry Update
~~~~~~~~~~~~~~~

.. code-block:: bash

    python 01_scripts/update_snap_geometry.py --config 02_config/parameters.yaml

Configuration File
-------------------

**Location:** ``02_config/parameters.yaml``

Study Area Section
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    study_area:
      name: "Study Area Name"
      wkt_geometry: "POLYGON ((lon1 lat1, lon2 lat2, ...))"
      subset_geometry: "POLYGON ((lon1 lat1, lon2 lat2, ...))"
      epsg_code: 4326

Download Section
~~~~~~~~~~~~~~~~

.. code-block:: yaml

    download:
      copernicus_user: "email@example.com"
      copernicus_password: "password"
      data_collection: "SENTINEL-2"
      product_type: "L1C"
      cloud_cover_threshold: 10
      default_start_date: "2025-05-01"
      default_end_date: "2025-06-30"

Processing Section
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    processing:
      c2rcc:
        valid_pixel_expression: "B8 > 0 && B8 < 0.1"
        salinity: 35.0
        temperature: 30.0
        ozone: 330.0
        pressure: 1000.0
        elevation: 20.0
        tsm_factor: 1.06
        tsm_exponent: 0.942
        chl_factor: 21.0
        chl_exponent: 1.04
      
      cdom:
        expression: "exp(0.544 * log(...)"
      
      resample:
        reference_band: "B2"
        upsampling: "Nearest"
        downsampling: "First"

Output Configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    output:
      formats:
        intermediate: "BEAM-DIMAP"
        final: "NetCDF4-BEAM"
        images: "PNG"
      
      visualization:
        dpi: 300
        transparent: true
        figsize: [10, 6]

Python API
----------

WaterQualityProcessor Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from process_pipeline import WaterQualityProcessor
    
    # Initialize
    processor = WaterQualityProcessor('02_config/parameters.yaml')
    
    # Run full pipeline
    processor.run_full_pipeline()
    
    # Or run individual steps
    processor.step_1_resample_subset()
    processor.step_2_reproject()
    processor.step_3_true_color()
    processor.step_4_c2rcc()
    processor.step_5_mosaic()
    processor.step_6_cdom_calculation()
    processor.step_7_generate_plots()

Key Methods
~~~~~~~~~~~

.. code-block:: python

    # Get tiles by date
    tiles_by_date = processor.get_tiles_by_date()
    # Returns: {'YYYYMMDD': {'single': [...], 'multiple': [...]}}
    
    # Extract date from filename
    date = processor.extract_date_from_filename('filename.nc')
    
    # Extract tile ID
    tile_id = processor.extract_block_name_from_filename('S2A_...T52LFL_...')

WaterQualityPlotter Class
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from plotting import WaterQualityPlotter
    
    # Initialize
    plotter = WaterQualityPlotter('02_config/parameters.yaml')
    
    # Plot individual parameters
    plotter.plot_chlorophyll()
    plotter.plot_tsm()
    plotter.plot_cdom()
    
    # Plot all
    plotter.generate_all_plots()

Update Geometry Function
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from update_snap_geometry import update_all_snap_geometries
    
    # Update all geometry files
    success = update_all_snap_geometries('02_config/parameters.yaml')

File Structure Documentation
----------------------------

Input Files
~~~~~~~~~~~

- ``02_config/parameters.yaml`` - Main configuration
- ``02_config/snap_graphs/*.xml`` - SNAP processing graphs
- ``03_raw_data/sentinel2_l1c/*.zip`` - Downloaded Sentinel-2 data

Output Files
~~~~~~~~~~~~

**Raw Processing:**

- ``04_processed_data/l2a_resampled/*.dim`` - Resampled data
- ``04_processed_data/l2a_reprojected/*.dim`` - Reprojected data
- ``04_processed_data/c2rcc_output/*.nc`` - C2RCC products
- ``04_processed_data/mosaic_output/*.nc`` - Mosaiced data (if multi-tile)
- ``04_processed_data/cdom_output/*.nc`` - CDOM products

**Final Products:**

- ``05_final_products/chl/*.png`` - Chlorophyll maps
- ``05_final_products/tsm/*.png`` - TSM maps
- ``05_final_products/cdom/*.png`` - CDOM maps
- ``05_final_products/true_color/*.png`` - RGB composites

**Logs:**

- ``06_logs/processing_*.log`` - Processing logs

Return Codes
------------

.. code-block:: text

    0 = Success
    1 = Failure
    
Example:

.. code-block:: bash

    python 01_scripts/process_pipeline.py --config ... --step 1
    echo $?  # Prints 0 or 1
