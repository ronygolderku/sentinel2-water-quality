# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------
project = 'Sentinel-2 Water Quality Processing Toolkit'
copyright = '2025, Md Rony Golder'
author = 'Md Rony Golder'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = []  # Remove static path since we don't have _static folder

# -- Options for MyST parser ------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
    "fieldlist",
]

# -- Theme options -----------------------------------------------------------
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': '#2980B9',
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# -- Source suffix ----------------------------------------------------------
source_suffix = {
    '.rst': None,
    '.md': None,
}

# -- Master doc --------------------------------------------------------------
master_doc = 'index'
