# Configuration file for Sphinx documentation builder
# For the full list of options, see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'Sentinel-2 Water Quality Processing Toolkit'
copyright = f'{datetime.now().year}, Md Rony Golder'
author = 'Md Rony Golder'
release = '1.0.0'
version = '1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
    'myst_parser',
]

# Source file extensions
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Master document
master_doc = 'index'

# Theme configuration
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
}

# HTML output options
html_static_path = ['_static']
html_logo = None
html_title = f'{project} Documentation'
html_favicon = None

# Napoleon settings (for Google/NumPy docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# Markdown support
myst_enable_extensions = [
    "colon_fence",
    "tasklist",
]

# Warnings
suppress_warnings = [
    'image.not_readable',
]
