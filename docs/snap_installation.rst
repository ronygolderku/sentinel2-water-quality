SNAP Installation Guide
=======================

Overview
--------

SNAP (Sentinel Application Platform) is required for all processing steps.

Download
--------

Visit: https://step.esa.int/main/download/snap-download/

Choose your operating system and download the latest version.

Installation By OS
------------------

Windows
~~~~~~~

1. Download the installer (``.exe`` file)
2. Run as Administrator
3. Follow the installation wizard
4. Choose installation directory (typically ``C:\Program Files\esa-snap``)
5. Complete installation

Linux (Ubuntu/Debian)
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Download the installer (.sh file)
    chmod +x esa-snap_sentinel_linux_64_10_0_0.sh
    sudo ./esa-snap_sentinel_linux_64_10_0_0.sh

Follow the prompts and install to ``/opt/snap`` or your preferred location.

macOS
~~~~~

1. Download the DMG file
2. Open the DMG
3. Drag SNAP.app to Applications folder
4. Installation complete

PATH Configuration
------------------

SNAP's ``gpt`` command must be in your system PATH.

Windows
~~~~~~~

1. Open Environment Variables:
   - Press ``Win + X`` and select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"

2. Under "System variables", select "Path" and click "Edit"

3. Click "New" and add:
   ``C:\Program Files\esa-snap\bin``

4. Click OK and restart your command prompt

Linux/macOS
~~~~~~~~~~~

Add to your shell profile (``~/.bashrc``, ``~/.zshrc``, or ``~/.profile``):

.. code-block:: bash

    export PATH="/opt/snap/bin:$PATH"

Then reload:

.. code-block:: bash

    source ~/.bashrc

Verification
~~~~~~~~~~~~

Test SNAP installation:

.. code-block:: bash

    gpt -h

Should display SNAP Graph Processing Tool help.

If not found:

1. Verify installation directory
2. Check PATH configuration
3. Restart command prompt/terminal
4. Try full path: ``C:\Program Files\esa-snap\bin\gpt -h`` (Windows)

Troubleshooting
---------------

**"gpt: command not found"**

- Check SNAP is installed
- Verify PATH configuration
- Restart terminal/command prompt

**"SNAP version too old"**

- Update to latest version from downloads page
- Uninstall old version first

**"Out of memory" errors**

- Increase SNAP heap memory in ``conf/snap.conf``
- Look for ``-Xmx`` parameter and increase value
- Requires SNAP restart

**GPU Support (Optional)**

For faster processing, enable GPU in SNAP:

- Windows: Open ``C:\Program Files\esa-snap\etc\snap.conf``
- Linux: Open ``/opt/snap/etc/snap.conf``
- Look for GPU settings and enable for your hardware

Next Steps
----------

After SNAP installation:

1. Verify with ``gpt -h``
2. Return to :doc:`getting_started`
3. Configure your study area in ``parameters.yaml``
4. Run first test: ``python validate_system.py``
