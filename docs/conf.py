from __future__ import annotations

project = "Doctree"
author = "Tim Camise"

source_suffix = ".rst"
master_doc = "index"
pygments_style = "sphinx"
html_static_path = ["_static"]
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    "sphinx.ext.autosectionlabel",
    "sphinxemoji.sphinxemoji",
]
html_theme = "sphinx_rtd_theme"
html_context = {
    "display_github": True,
}
add_module_names = False
inheritance_graph_attrs = dict(rankdir="BT", center="true")
inheritance_node_attrs = dict(color="dodgerblue1", style="filled")
autodoc_default_options = {
    "members": True,
}

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.

# Extract version set from pyproject.toml
import importlib.metadata as importlib_metadata

version = importlib_metadata.version("doctree")
