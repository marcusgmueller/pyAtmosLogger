# Configuration file for the Sphinx documentation builder.
import sphinx_book_theme
import sys
import os
# -- Project information
sys.path.insert(0, os.path.abspath('..'))
project = 'pyAtmosLogger'
copyright = '2023, Müller'
author = 'Marcus G. Müller'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']
html_static_path = ["_static"]

# -- Options for HTML output

html_theme = 'sphinx_book_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

html_logo = "_static/images/pyAtmosLogger.png"