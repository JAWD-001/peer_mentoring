import os
import sys

import django

# Add your Django project's root directory to the Python path
sys.path.insert(0, os.path.abspath(".."))

# Configure the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "peer_mentoring.settings")
django.setup()

# -- General configuration ------------------------------------------------

# Project information
project = "Peer Mentoring"
author = "James Dycus"

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
]

# Templates
templates_path = ["_templates"]

# Source file patterns
exclude_patterns = []

# -- Options for HTML output ----------------------------------------------

# Theme
html_theme = "sphinx_rtd_theme"

# HTML theme options
html_theme_options = {}

# Output directory for HTML build
html_output = "_build/html"

# -- Autodoc configuration ------------------------------------------------

# Auto-generate documentation from docstrings
autodoc_member_order = "bysource"
autodoc_typehints = "none"

# -- Options for internationalization -------------------------------------

# Language
language = "en"

# -- Extensions ------------------------------------------------------------

# Enable autodoc extension
extensions = ["sphinx.ext.autodoc"]

# -- HTML theme options ---------------------------------------------------

# Custom HTML context
html_context = {
    "display_github": True,
    "github_user": "JAWD-001",
    "github_repo": "peer_mentoring",
    "github_version": "master/docs/",
}

# -- HTML static path -----------------------------------------------------

# Static files
html_static_path = ["_static"]
