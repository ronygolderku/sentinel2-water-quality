Setup Guide
===========

Detailed Configuration Instructions
------------------------------------

The workflow is designed to be **study-area agnostic**. You only need to update four things:

1. Study area WKT geometry
2. Copernicus credentials
3. Date range (optional)
4. Cloud cover threshold (optional)

Study Area Configuration
------------------------

Your study area must be defined as a **WKT POLYGON** with coordinates in **(longitude, latitude)** order:

.. code-block:: yaml

    POLYGON ((lon1 lat1, lon2 lat2, lon3 lat3, lon4 lat4, lon1 lat1))

**Important:**

- Longitude is **X** (horizontal) - ranges from -180 to +180
- Latitude is **Y** (vertical) - ranges from -90 to +90

Getting Coordinates
~~~~~~~~~~~~~~~~~~~

**Option A: Online Tool (Recommended)**

1. Visit `geojson.io <https://geojson.io/>`_
2. Draw a polygon around your study area
3. Copy the coordinates from the left panel
4. Convert to WKT format: ``POLYGON ((lon lat, lon lat, ...))``

**Option B: QGIS**

1. Draw a rectangle or polygon
2. Right-click → Copy as WKT
3. Paste directly into parameters.yaml

**Option C: Manual**

Get the corner coordinates and format as:

.. code-block:: yaml

    POLYGON ((min_lon min_lat, max_lon min_lat, max_lon max_lat, min_lon max_lat, min_lon min_lat))

Example Study Areas
~~~~~~~~~~~~~~~~~~~~

**Western Australia Coast (Single-tile):**

.. code-block:: yaml

    wkt_geometry: "POLYGON ((115.54 -31.93, 115.79 -31.93, 115.79 -32.26, 115.54 -32.26, 115.54 -31.93))"

**Great Barrier Reef (Multi-tile):**

.. code-block:: yaml

    wkt_geometry: "POLYGON ((142.0 -10.0, 156.0 -10.0, 156.0 -24.0, 142.0 -24.0, 142.0 -10.0))"

**Baltic Sea, Europe:**

.. code-block:: yaml

    wkt_geometry: "POLYGON ((9.0 53.0, 30.0 53.0, 30.0 66.0, 9.0 66.0, 9.0 53.0))"

Credent Configuration
---------------------

.. code-block:: yaml

    download:
      copernicus_user: "your_email@example.com"
      copernicus_password: "your_password"
      cloud_cover_threshold: 10
      default_start_date: "2025-05-01"
      default_end_date: "2025-06-30"

Processing Parameters
---------------------

Most parameters have good defaults for water quality studies:

.. code-block:: yaml

    processing:
      c2rcc:
        salinity: 35.0
        temperature: 30.0
        tsm_factor: 1.06
        chl_factor: 21.0
      
      cdom:
        expression: "exp(0.544 * log(...)"

Automatic Geometry Updates
---------------------------

Once you set the WKT in parameters.yaml, the workflow automatically:

1. ✅ Extracts geographic bounds
2. ✅ Updates ``resample_subset.xml`` with WKT
3. ✅ Updates ``mosaic.xml`` with bounds
4. ✅ All SNAP files sync automatically
5. ✅ Processing uses correct study area

**No manual XML editing needed!**

Manual Update (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~

To manually update geometry files:

.. code-block:: bash

    python 01_scripts/update_snap_geometry.py --config 02_config/parameters.yaml

Verification
------------

After configuration, verify the setup:

.. code-block:: bash

    python validate_system.py

This will check:

- ✅ Python dependencies
- ✅ SNAP installation
- ✅ Configuration files
- ✅ Directory structure
- ✅ SNAP geometry files
