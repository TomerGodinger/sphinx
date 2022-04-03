# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import pathlib
import sys
sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())


# -- Project information -----------------------------------------------------

project = 'LuCLI'
copyright = '2022, Nomnom Inc.'
author = 'Sanji'

# The full version, including alpha/beta/rc tags
# This is taken from the BUILD_VERSION environment variable, with the
# constant value here used as default if the variable is missing
release = 'main'
# release = pathlib.Path('BUILD_VERSION').read_text()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_markdown_builder',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx_click',
    'sphinx_autodoc_typehints',
    'sphinxcontrib.restbuilder',
    'sphinx_multiversion',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "versioning.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html"
    ]
}

# html_sidebars = {
#     '**': [
#         'localtoc.html', 'relations.html', 'sourcelink.html', 'searchbox.html',
#         # 'versioning.html',
#     ],
# }

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']



# -- Options for versioning --------------------------------------------------
smv_outputdir_format = 'versions/{ref.name}'



# ----------------------------------------------------------------------------
# -- Extra Documenter for Simple Docstrings ----------------------------------
# -- Taken from: https://stackoverflow.com/questions/7825263/including-docstring-in-sphinx-documentation
# ----------------------------------------------------------------------------
from sphinx.ext import autodoc

class SimpleDocumenter(autodoc.MethodDocumenter):
    objtype = "simple"

    #do not indent the content
    content_indent = ""

    #do not add a header to the docstring
    def add_directive_header(self, sig):
        pass

def setup(app):
    app.add_autodocumenter(SimpleDocumenter)
