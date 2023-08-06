# Copyright 2020-2020, Kostis Anagnostopoulos;
# Licensed under the terms of the Apache License, Version 2.0. See the LICENSE file associated with the project for terms.
"""
Extends Sphinx with :rst:dir:`graphtik` directive for :term:`plotting <plotter>` from doctest code.
"""
import collections.abc as cabc
import itertools as itt
import os
import re
from collections import defaultdict
from pathlib import Path
from shutil import copyfileobj
from typing import Dict, List, Set, Union, cast

import sphinx
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst import roles as rst_roles
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.domains import Domain, Index, ObjType
from sphinx.domains.std import StandardDomain
from sphinx.environment import BuildEnvironment
from sphinx.ext import doctest as extdoctest
from sphinx.ext.autodoc import ModuleDocumenter
from sphinx.locale import _, __
from sphinx.roles import XRefRole
from sphinx.util import inspect
from sphinx.util import logging
from sphinx.util.console import bold  # pylint: disable=no-name-in-module
from sphinx.writers.html import HTMLTranslator
from sphinx.writers.latex import LaTeXTranslator

from graphtik.fnop import FnOp
from graphtik.plot import default_jupyter_render

from .. import __version__

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Use backported to PY<3.7 `importlib_resources` lib.
    import importlib_resources as pkg_resources  # noqa

obj_name = "graphtik diagram"
role_name = "graphtik"
log = logging.getLogger(__name__)


class graphtik_node(nodes.General, nodes.Element):
    """Non-writtable node wrapping (literal-block + figure(dynaimage)) nodes.

    The figure gets the :name: & :align: options, the contained dynaimage gets
    the :height", :width:, :scale:, :classes: options.
    """


def _ignore_node_but_process_children(
    self: HTMLTranslator, node: graphtik_node
) -> None:
    raise nodes.SkipDeparture


class dynaimage(nodes.General, nodes.Inline, nodes.Element):
    """Writes a tag in `tag` attr (``<img>`` for PNGs, ``<object>`` for SVGs/PDFs). """


def _zoomable_activation_js_code(default_zoom_opts: str) -> str:
    if not default_zoom_opts:
        default_zoom_opts = "{}"

    return f"""
    $(function() {{
        var default_opts = {default_zoom_opts};
        for (const svg_el of $( ".graphtik-zoomable-svg" )) {{
            var zoom_opts = ("svgZoomOpts" in svg_el.dataset?
                                svg_el.dataset.svgZoomOpts:
                                default_opts);
            svg_el.addEventListener("load", function() {{
                // Still fails for Chrome localy :-()
                var panZoom = svgPanZoom(svg_el, zoom_opts);

                // Container follows window size.
                $(window).resize(function(){{
                    panZoom.resize();
                    panZoom.fit();
                    panZoom.center();
                }});
            }});
        }};
    }});
    """


def _enact_zoomable_svg(self: HTMLTranslator, node: dynaimage, tag: str):
    """Make SVGs zoomable if enabled by option/config.

    :param node:
        Assign a special *class* for the zoom js-code to select by it.

    NOTE: does not work locally with chrome: ariutta/svg-pan-zoom#326
    """
    if tag == "object" and "graphtik-zoomable-svg" in node["classes"]:
        ## # Setup pan+zoom JS-code only once.
        #
        if not hasattr(self.builder, "svg_zoomer_doc_scripts"):
            self.builder.add_js_file(
                "https://ariutta.github.io/svg-pan-zoom/dist/svg-pan-zoom.min.js"
            )
            self.builder.add_js_file(
                None,
                type="text/javascript",
                body=_zoomable_activation_js_code(
                    self.config.graphtik_zoomable_options
                ),
            )

            # Mark actions above as preformed only once.
            self.builder.svg_zoomer_doc_scripts = True


def _html_visit_dynaimage(self: HTMLTranslator, node: dynaimage):
    # See sphinx/writers/html5:visit_image()
    tag = getattr(node, "tag", None)
    if not tag:
        # Probably couldn't find :graphvar: in doctest globals.
        raise nodes.SkipNode
    assert tag in ["img", "object"], (tag, node)

    _enact_zoomable_svg(self, node, tag)

    atts = {k: v for k, v in node.attlist() if k not in nodes.Element.known_attributes}
    self.body.extend([self.emptytag(node, tag, "", **atts), f"</{tag}>"])

    cmap = getattr(node, "cmap", "")
    if cmap:
        self.body.append(cmap)

    raise nodes.SkipNode


def _latex_visit_dynaimage(self: LaTeXTranslator, node: dynaimage) -> None:
    if not getattr(node, "tag", None):
        # Probably couldn't find :graphvar: in doctest globals.
        raise nodes.SkipNode

    pnode: nodes.figure = node.parent

    is_inline = self.is_inline(node)

    if not is_inline:
        pre = ""
        post = ""
        if "align" in pnode:
            if "left" in pnode["align"]:
                pre = "{"
                post = r"\hspace*{\fill}}"
            elif "right" in pnode["align"]:
                pre = r"{\hspace*{\fill}"
                post = "}"
            elif "center" in pnode["align"]:
                pre = r"{\hfill"
                post = r"\hspace*{\fill}}"
        self.body.append("\n%s" % pre)

    fname = node.get("data", node.get("src"))
    self.body.append(r"\sphinxincludegraphics[]{%s}" % fname)

    if not is_inline:
        self.body.append("%s\n" % post)

    raise nodes.SkipNode


_image_formats = ("png", "svg", "svgz", "pdf", None)


def _valid_format_option(argument: str) -> Union[str, None]:
    # None choice ignored, choice() would scream due to upper().
    if not argument:
        return None
    return directives.choice(argument, _image_formats)


def _tristate_bool_option(val: str) -> Union[None, bool]:
    """
    A parsing function for a tri-state boolean option.

    :raise ValueError:
        if not one of: `None`, true, 1, yes, on, false, 0, no, off
    """
    val = val and val.strip().lower()
    if not val:
        return None
    if val in "true 1 yes on".split():
        return True
    if val in "false 0 no off".split():
        return False
    raise ValueError(f"invalid boolean {val!r} supplied")


_graphtik_options = {
    "caption": directives.unchanged,
    "graph-format": _valid_format_option,
    "graphvar": directives.unchanged_required,
    "zoomable": _tristate_bool_option,
    "zoomable-opts": directives.unchanged,
}
_doctest_options = extdoctest.DoctestDirective.option_spec
_img_options = {
    k: v
    for k, v in directives.images.Image.option_spec.items()
    if k not in ("name", "align")
}
_fig_options = {
    k: v
    for k, v in directives.images.Figure.option_spec.items()
    if k in ("name", "figclass", "align", "figwidth")
}
_option_spec = {
    **_doctest_options,
    **_img_options,
    **_fig_options,
    **_graphtik_options,
}


class _GraphtikTestDirective(extdoctest.TestDirective):
    """
    A doctest-derrived directive embedding graphtik plots into a sphinx site.

    Nodes::

        graphtik:               ignored, just to kick-in processing
            doctest-node:       original nodes, literal or doctest
            figure
                target:         if :name: present
                dynaimage:      rendered as <img> or <object>
                caption:        if :caption: or :name: present

    """

    _real_name: str
    _con_name: str
    #: Adapted from: :meth:`sphinx.registry.SphinxComponentRegistry.add_crossref_type()`
    indextemplate = f"pair: %s; {obj_name}"

    def run(self) -> List[nodes.Node]:
        """Con :class:`.TestDirective` it's some subclass, and append custom options in return node."""
        options = self.options

        ## Empty directive would add an empty literal line.
        #  (common, just to print a graphvar global from a previous doctest)
        #
        if not "\n".join(self.content).strip():
            options["hide"] = True

        self.name = self._con_name
        try:
            original_nodes = super().run()
        finally:
            self.name = self._real_name

        location = self.state_machine.get_source_and_line(self.lineno)

        img_format = self._decide_img_format(options)
        log.debug("decided `graph-format`: %r", img_format, location=location)
        if not img_format:
            # Bail out, probably unknown builder.
            return original_nodes

        node = graphtik_node(graphvar=options.get("graphvar"), img_format=img_format)
        node.source, node.line = location
        ## Decide a unique filename (and id).
        #
        name = options.get("name") or ""
        if name:
            name = nodes.fully_normalize_name(name)
        targetname = (
            f"graphtik-{self.env.docname}-{name}-{self.env.new_serialno('graphtik')}"
        )
        node["filename"] = targetname
        node += original_nodes

        figure = nodes.figure()
        figure.source, figure.line = location
        align = options.get("align")
        if align:
            align = f"align-{align}"
            figure["classes"].append(align)
        figure["classes"].extend(options.get("figclass", "").split())
        node += figure

        # TODO: emulate sphinx-processing for image width & height attrs.
        img_attrs = {k: v for k, v in options.items() if k in _img_options}
        image = dynaimage(**img_attrs)
        image.source, image.line = location
        image["classes"].extend(options.get("class", "").split())
        #  TODO: TCs for zooamble-SVGs options & configs.
        if "svg" in img_format:
            zoomable = options.get("zoomable")
            if zoomable is None:
                zoomable = self.config.graphtik_zoomable
                if zoomable:
                    image["classes"].append("graphtik-zoomable-svg")
        ## Assign a special *dataset* html-attribute
        #  with the content of a respective option.
        #
        zoomable_options = options.get("zoomable-opts")
        if zoomable_options:
            image["data-svg-zoom-opts"] = zoomable_options
        figure += image

        # A caption is needed if :name: is given, to create a permalink on it
        # (see sphinx/writers/html:HTMLTranslator.depart_caption()),
        # so get it here, not to overwrite it with :name: (if given below).`
        caption = options.get("caption")

        ## Prepare target,
        #
        if "name" in options:
            ##  adapted from: self.add_name()
            #
            name = options.pop("name")
            if not caption:
                caption = name
            figure["names"].append(targetname)
            ## adapted from: sphinx.domains.std.Target directive.
            #
            std = cast(StandardDomain, self.env.get_domain("std"))
            ## Suppress warning on duplicates (replaced with INFO).
            #  Duplicates occur either by include directives
            #  or because :noindex: in autoclass is ignored here.
            #
            objtype = "graphtik"
            if (objtype, name) in std.objects:
                docname = std.objects[objtype, name][0]
                log.info(
                    __("Skipping duplicate %s description of %s, other instance in %s"),
                    objtype,
                    name,
                    docname,
                    location=location,
                )
            else:
                std.note_object(objtype, name, targetname, figure)

        ## See sphinx.ext.graphviz:figure_wrapper(),
        #  and <sphinx.git>/tests/roots/test-add_enumerable_node/enumerable_node.py:MyFigure
        #
        if caption:
            inodes, messages = self.state.inline_text(caption, self.lineno)
            caption_node = nodes.caption(caption, "", *inodes)
            self.set_source_info(caption_node)
            caption_node += messages
            figure += caption_node

        return [node]

    def _decide_img_format(self, options):
        img_format = None
        if "graph-format" in options:
            img_format = options["graph-format"]
        else:
            img_format = self.config.graphtik_default_graph_format
        if not img_format:
            builder_name = self.env.app.builder.name
            for regex, fmt in self.config.graphtik_graph_formats_by_builder.items():
                if re.search(regex, builder_name):
                    img_format = fmt
                    break
            else:
                log.debug(
                    "builder-name %r did not match any key in `graphtik_graph_formats_by_builder`"
                    ", no plot will happen",
                    builder_name,
                )

        return img_format


class GraphtikDoctestDirective(_GraphtikTestDirective):
    """Embeds plots from doctest code (see :rst:dir:`graphtik`). """

    option_spec = _option_spec
    _real_name = "graphkit"
    _con_name = "doctest"


class GraphtikTestoutputDirective(_GraphtikTestDirective):
    """Like :rst:dir:`graphtik` directive, but  emulates doctest :rst:dir:`testoutput` blocks. """

    option_spec = _option_spec
    _real_name = "graphtik-output"
    _con_name = "testoutput"


def _should_work(app: Sphinx):
    """Avoid event-callbacks if not producing HTML/Latex."""
    builder_name = app.builder.name
    builder_name_regexes = app.config.graphtik_graph_formats_by_builder.keys()
    return any(re.search(regex, builder_name) for regex in builder_name_regexes)


def _run_doctests_on_graphtik_document(app: Sphinx, doctree: nodes.Node):
    """Callback of `doctree-resolved`` event. """
    try:
        docname = app.env.docname
        from ._graphtikbuilder import get_graphtik_builder

        if _should_work(app) and any(doctree.traverse(graphtik_node)):
            log.info(__("Graphtik-ing document %r..."), docname)
            graphtik_builder = get_graphtik_builder(app)
            graphtik_builder.test_doc(docname, doctree)
    except Exception as ex:
        log.error("General failure of Graphtik-sphinx extension: %s", ex, exc_info=True)
        raise


class DocFilesPurgatory:
    """Keeps 2-way associations of docs <--> abs-files, to purge them."""

    #: Multi-map: docnames -> abs-file-paths
    doc_fpaths: Dict[str, Set[Path]]

    def __init__(self):
        self.doc_fpaths = defaultdict(set)

    def register_doc_fpath(self, docname: str, fpath: Path):
        """Must be absolute, for purging to work."""
        self.doc_fpaths[docname].add(fpath)

    def purge_doc(self, docname: str):
        """Remove doc-files not used by any other doc."""
        doc_fpaths = self.doc_fpaths

        for fpath in doc_fpaths.get(docname, ()):
            docs_involved = set(
                docs for docs, fpaths in doc_fpaths.items() if fpath in fpaths
            )
            assert docname in docs_involved, (docname, docs_involved)

            ## Delete file when given `docname` is the only document using it.
            #
            if len(docs_involved) == 1:  # equality checked also by assertion

                try:
                    log.debug(
                        "Deleting outdated image '%s' of doc %r...", docname, fpath
                    )
                    fpath.unlink()
                except Exception as ex:
                    log.warning(
                        "Ignoring error while deleting outdated fpath '%s': %s",
                        fpath,
                        ex,
                    )

        doc_fpaths.pop(docname, None)

    def __getstate__(self) -> Dict:
        """Obtains serializable data for pickling."""
        return self.doc_fpaths

    def __setstate__(self, state: Dict) -> None:
        """Restore serialized data for pickling."""
        self.doc_fpaths = state


def _purge_old_document_images(app: Sphinx, env: BuildEnvironment, docname: str):
    img_registry: DocFilesPurgatory = getattr(env, "graphtik_image_purgatory", None)
    if img_registry:
        try:
            env.graphtik_image_purgatory.purge_doc(docname)
        except Exception as ex:
            app.logger.error(
                bold(__("Failed purging old images due to: %s")), ex, exc_info=ex
            )

    else:
        env.graphtik_image_purgatory = DocFilesPurgatory()


def _stage_my_pkg_resource(inp_fname, out_fpath):
    with pkg_resources.open_binary(__package__, inp_fname) as inp, open(
        out_fpath, "wb"
    ) as out:
        copyfileobj(inp, out)


_css_fname = "graphtik.css"


def _copy_graphtik_static_assets(app: Sphinx, exc: Exception) -> None:
    """Callback of `build-finished`` event. """
    if not exc and _should_work(app):
        dst = Path(app.outdir, "_static", _css_fname)
        ## Builder `latex` does not have _static folder.
        #
        if not dst.exists() and dst.parent.exists():
            _stage_my_pkg_resource(_css_fname, dst)


def _validate_and_apply_configs(app: Sphinx, config: Config):
    """Callback of `config-inited`` event. """
    config.graphtik_default_graph_format is None or _valid_format_option(
        config.graphtik_default_graph_format
    )


def _teach_documenter_about_operations(FuncDocClass):
    original__can_document_member = FuncDocClass.can_document_member

    def patched__can_document_member(cls, member, membername, isattr, parent):
        return original__can_document_member(member, membername, isattr, parent) or (
            isinstance(member, FnOp) and isinstance(parent, ModuleDocumenter)
        )

    FuncDocClass.can_document_member = classmethod(patched__can_document_member)


def process_fnop_signature(app, what, name, obj, options, signature, return_annotation):
    try:
        if isinstance(obj, FnOp):
            fn = obj.fn
            fn_sig = inspect.signature(fn)
            signature = str(fn_sig)
            return_annotation = None
    except Exception as ex:
        log.error("Failed `autodoc-process-signature`: %s", ex, exc_info=1)
    return (signature, return_annotation)


def _setup_autodoc(app: Sphinx):
    app.setup_extension("sphinx.ext.autodoc")

    _teach_documenter_about_operations(app.registry.documenters["function"])
    app.connect("autodoc-process-signature", process_fnop_signature)


def _setup_directive(app: Sphinx):
    app.setup_extension("sphinx.ext.doctest")
    app.add_config_value(
        "graphtik_graph_formats_by_builder",
        {"html": "svg", "readthedocs": "svg", "latex": "pdf"},
        "html",
        [cabc.Mapping],
    )
    app.add_config_value("graphtik_default_graph_format", None, "html", [str, None])
    app.add_config_value("graphtik_plot_keywords", {}, "html", [cabc.Mapping])
    app.add_config_value("graphtik_zoomable", True, "html", [bool])
    app.add_config_value("graphtik_warning_is_error", False, "html", [bool])
    app.add_config_value("graphtik_save_dot_files", None, "html", [bool])
    app.add_config_value(
        "graphtik_zoomable_options",
        default_jupyter_render["svg_pan_zoom_json"],
        "html",
        [str],
    )

    app.add_node(
        graphtik_node,
        **dict.fromkeys(
            "html latex text man texinfo".split(),
            (_ignore_node_but_process_children, None),
        ),
    )
    app.add_node(
        dynaimage,
        html=(_html_visit_dynaimage, None),
        latex=(_latex_visit_dynaimage, None),
        **dict.fromkeys(
            "text man texinfo".split(), (_ignore_node_but_process_children, None)
        ),
    )

    ## Support cross-referencing graphs by their :name: option.
    #  Addapted from `sphinx.registry.SphinxComponentRegistry.add_crossref_type()``
    #  to keep our directives.
    #
    app.add_role_to_domain("std", role_name, XRefRole())
    obj_type = ObjType(obj_name, role_name)
    object_types = app.registry.domain_object_types.setdefault("std", {})
    for dir_name, directive in (
        ("graphtik", GraphtikDoctestDirective),
        ("graphtik-output", GraphtikTestoutputDirective),
    ):
        app.add_directive(dir_name, directive)
        object_types[dir_name] = obj_type

    app.connect("config-inited", _validate_and_apply_configs)
    app.connect("doctree-read", _run_doctests_on_graphtik_document)
    app.connect("env-purge-doc", _purge_old_document_images)
    app.connect("build-finished", _copy_graphtik_static_assets)

    app.add_css_file(_css_fname)

    # Permanently set this, or else, e.g. +SKIP will not work!
    app.config.trim_doctest_flags = False


def setup(app: Sphinx):
    setup.app = app
    app.require_sphinx("2.0")

    _setup_autodoc(app)
    _setup_directive(app)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
