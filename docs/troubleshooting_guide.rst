Troubleshooting Guide
=====================

Common Issues
-------------

SNAP GPT Not Found
~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

    gpt: command not found

**Solution:**

1. Verify SNAP installation:

.. code-block:: bash

    which gpt              # Linux/macOS
    where gpt              # Windows

2. If not found, add to PATH:

   - **Windows**: Add ``C:\Program Files\esa-snap\bin`` to System PATH
   - **Linux/macOS**: Add to ``~/.bashrc``: ``export PATH="/opt/snap/bin:$PATH"``

3. Restart terminal/command prompt

Python Package Errors
~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

    ModuleNotFoundError: No module named 'xarray'

**Solution:**

.. code-block:: bash

    pip install -r requirements.txt

Or install individual packages:

.. code-block:: bash

    pip install xarray numpy matplotlib cartopy

Authentication Failed
~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

    401 Unauthorized: Invalid credentials

**Solution:**

1. Verify Copernicus credentials in ``02_config/parameters.yaml``
2. Check username and password spelling
3. Verify account is active at https://identity.dataspace.copernicus.eu/
4. Reset password if needed

Download Errors
~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

    No data found for study area

**Possible Causes:**

- Study area not covered by Sentinel-2
- Date range has no acquisitions
- Cloud cover too high
- Area too small or incorrectly specified

**Solution:**

1. Verify WKT geometry is correct
2. Check date range is reasonable (e.g., 2016 onwards)
3. Access `Sentinel Hub <https://www.sentinel-hub.com/>`_ to verify data availability
4. Lower cloud_cover_threshold

Processing Errors
~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

    Step X failed: [error details]

**Solution:**

1. Check logs in ``06_logs/`` for detailed error messages
2. Verify input data exists
3. Check disk space (minimum 10GB free)
4. Verify SNAP installation is working
5. Try running individual step: ``python process_pipeline.py --config ... --step 1``

Memory Errors
~~~~~~~~~~~~~

**Error:**

.. code-block:: text

    MemoryError or OutOfMemoryException

**Solution:**

1. **Increase SNAP heap memory:**

   - Open ``C:\Program Files\esa-snap\etc\snap.conf`` (Windows)
   - Find line: ``-Xmx16G`` (or similar)
   - Increase value: ``-Xmx32G`` or ``-Xmx64G``
   - Restart SNAP

2. **Reduce processing area:**

   - Make study area smaller
   - Process fewer tiles at once

3. **Close other applications** to free system RAM

No Output Files
~~~~~~~~~~~~~~~

**Problem:**

Processing completes but no output files generated.

**Solution:**

1. Check logs: ``tail -f 06_logs/processing_*.log``
2. Verify input data exists in ``03_raw_data/``
3. Check ``04_processed_data/`` subdirectories for intermediate outputs
4. Verify write permissions on output directories
5. Run validation: ``python validate_system.py``

Geometry Update Issues
~~~~~~~~~~~~~~~~~~~~~~

**Problem:**

XML files not updating with study area.

**Solution:**

Manual update:

.. code-block:: bash

    python 01_scripts/update_snap_geometry.py --config 02_config/parameters.yaml

Verify output shows:

.. code-block:: text

    ✓ Updated resample_subset.xml with new geometry
    ✓ Updated mosaic.xml with bounding box

Mosaic Not Creating
~~~~~~~~~~~~~~~~~~~

**Problem:**

Multi-tile processing but no mosaic file created.

**Causes:**

- Not enough tiles for study date
- Mosaic bounds not set correctly
- SNAP GPT failure

**Solution:**

1. Verify you have multiple tiles for the date
2. Check log for mosaic step details
3. Manually verify bounds in ``02_config/snap_graphs/mosaic.xml``
4. Try running step 5 individually:

.. code-block:: bash

    python process_pipeline.py --config 02_config/parameters.yaml --step 5

Plots Not Generating
~~~~~~~~~~~~~~~~~~~~

**Problem:**

No PNG files in ``05_final_products/``

**Solutions:**

1. Check intermediate products exist:

   - ``04_processed_data/c2rcc_output/`` for single-tile
   - ``04_processed_data/mosaic_output/`` for multi-tile

2. Verify CDOM step completed successfully (step 6)

3. Run plotting manually:

.. code-block:: bash

    python 01_scripts/plotting.py --config 02_config/parameters.yaml

System Validation
-----------------

Use the validation script to diagnose issues:

.. code-block:: bash

    python validate_system.py

This checks:

- ✅ Python packages
- ✅ SNAP installation
- ✅ Configuration files
- ✅ Directory structure
- ✅ Write permissions
- ✅ SNAP XML files

Log File Analysis
-----------------

Processing logs are in ``06_logs/`` with format:

.. code-block:: text

    processing_YYYYMMDD_HHMMSS.log

View recent logs:

.. code-block:: bash

    tail -f 06_logs/processing_*.log

Look for:

- SUCCESS/FAILED status
- ERROR entries (red in terminal)
- File counts completed
- Errors for specific steps

Getting Help
------------

1. **Check Documentation:** See ``07_documentation/`` or online docs
2. **Review Logs:** Detailed error messages in ``06_logs/``
3. **Run Diagnostics:** Execute ``validate_system.py``
4. **Check Examples:** Review sample outputs in repository
5. **SNAP Issues:** Consult `SNAP Documentation <https://step.esa.int/main/doc/>`_

Common Parameter Values
------------------------

**For Australian Coastal Waters:**

.. code-block:: yaml

    processing:
      c2rcc:
        salinity: 35.0
        temperature: 30.0
        tsm_factor: 1.06
        chl_factor: 21.0

**For Other Regions:**

Adjust temperature and salinity for your water type.

**Cloud Cover:**

- Tropical: 15-20 (higher variability)
- Temperate: 10 (default, good)
- Polar: 5-10 (higher quality needed)
