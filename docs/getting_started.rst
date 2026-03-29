Getting Started
===============

Requirements
------------

**Software:**

- Python 3.8+ (tested with Python 3.12)
- SNAP (Sentinel Application Platform)
- Git (optional, for cloning)

**System:**

- Windows 10/11, Linux, or macOS
- RAM: 8GB minimum, 16GB recommended
- Storage: 10GB+ free space
- Internet connection for data download

**Copernicus Account:**

Create a free account at `Copernicus Data Space Ecosystem <https://identity.dataspace.copernicus.eu/>`_

Installation Steps
------------------

1. **Clone Repository**

.. code-block:: bash

    git clone https://github.com/ronygolderku/sentinel2-water-quality.git
    cd sentinel2-water-quality

2. **Install Python Dependencies**

.. code-block:: bash

    pip install -r requirements.txt

3. **Install SNAP**

- Download from `ESA STEP <https://step.esa.int/main/download/snap-download/>`_
- Install as Administrator (Windows) or with sudo (Linux/macOS)
- Add to PATH:
  
  - **Windows**: ``C:\Program Files\esa-snap\bin``
  - **Linux/macOS**: ``/usr/local/snap/bin``

- Verify installation:

.. code-block:: bash

    gpt -h

4. **Configure Study Area**

Edit ``02_config/parameters.yaml``:

.. code-block:: yaml

    study_area:
      name: "Your Study Area"
      wkt_geometry: "POLYGON ((lon1 lat1, lon2 lat2, lon3 lat3, lon4 lat4, lon1 lat1))"
    
    download:
      copernicus_user: "your_email@example.com"
      copernicus_password: "your_password"

5. **First Run**

.. code-block:: bash

    # Test with a small sample
    python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml --step 1

See :doc:`setup_guide` for detailed examples and coordinate help.
