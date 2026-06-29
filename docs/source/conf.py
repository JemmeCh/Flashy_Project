# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../../src/flashy'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'FLASHy'
copyright = '2026, Jean-Emmanuel Chouinard'
author = 'Jean-Emmanuel Chouinard'
release = '1.0.3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "msgspec": ("https://msgspec.dev/", None),
    "qt": ("https://doc.qt.io/qtforpython/", None),
}

extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = []

automodule_options = {'members', 'undoc-members'}

autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented_params"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

def skip_qt_internals(app, what, name, obj, skip, options):
    qt_noise = {
        "staticMetaObject",
        "qt_metacall",
        "qt_metacast",
        "metaObject",
    }
    
    if name in qt_noise:
        return True
    
    return skip

def setup(app):
    app.connect("autodoc-skip-member", skip_qt_internals)