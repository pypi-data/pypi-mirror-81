# Copyright 2016, Yahoo Inc.
# Licensed under the terms of the Apache License, Version 2.0. See the LICENSE file associated with the project for terms.

import logging
import re
from collections import OrderedDict, namedtuple
from functools import partial
from textwrap import dedent
from types import SimpleNamespace

import pandas as pd
import pytest

from graphtik import (
    NO_RESULT,
    NO_RESULT_BUT_SFX,
    compose,
    implicit,
    keyword,
    operation,
    optional,
    sfx,
    sfxed,
    vararg,
    varargs,
    vcat,
)
from graphtik.config import (
    operations_endured,
    operations_reschedullled,
    tasks_in_parallel,
    tasks_marshalled,
)
from graphtik.fnop import FnOp, Operation, as_renames, reparse_operation_data
from graphtik.modifier import dep_renamed
from graphtik.planning import yield_ops

from .helpers import oneliner


@pytest.fixture(params=[None, "got"])
def opname(request):
    return request.param


@pytest.fixture(params=[None, "some"])
def opneeds(request):
    return request.param


@pytest.fixture(params=[None, "stuff"])
def opprovides(request):
    return request.param


def test_repr_smoke(opname, opneeds, opprovides):
    # Simply check __repr__() does not crash on partial attributes.
    kw = locals().copy()
    kw = {name[2:]: arg for name, arg in kw.items()}

    op = operation(**kw)
    str(op)


def test_repr_returns_dict():
    assert (
        str(operation(lambda: None, name="", returns_dict=True))
        == "FnOp(name='', fn{}='<lambda>')"
    )
    assert (
        str(operation(lambda: None, name="myname"))
        == "FnOp(name='myname', fn='<lambda>')"
    )


def test_auto_func_name():
    assert operation(lambda: None).name == "<lambda>"
    assert operation(partial(lambda a: None)).name == "<lambda>(...)"


def test_builder_pattern():
    opb = operation()
    assert not isinstance(opb, FnOp)
    assert str(opb).startswith("<function FnOp.withset at")

    assert str(opb(sum)) == "FnOp(name='sum', fn='sum')"

    assert str(opb(name="K")) == "FnOp(name='K', fn='identity_fn')"

    op = opb.withset(needs=["a", "b"])
    assert isinstance(op, FnOp)
    assert str(op) == "FnOp(name=None, needs=['a', 'b'], fn=None)"
    with pytest.raises(ValueError, match=f"Operation must have a callable `fn` and"):
        op.compute({})

    op = op.withset(provides="SUM", fn=sum, name=None)
    assert str(op) == "FnOp(name='sum', needs=['a', 'b'], provides=['SUM'], fn='sum')"

    op = op.withset(provides="s", needs="a", fn=str)
    assert str(op) == "FnOp(name='sum', needs=['a'], provides=['s'], fn='str')"


@pytest.mark.parametrize(
    "opargs, exp",
    [
        ((None, None, None), (None, (), ())),
        ## Check name
        (("_", "a", ("A",)), ("_", ("a",), ("A",))),
        (("", ("a",), None), ("", ("a",), ())),
        (("a", "a", "b"), ("a", ("a",), ("b",))),
        (("a", None, None), ("a", (), ())),
        ## Check needs
        (("", (), None), ("", (), ())),
        (("", [], None), ("", [], ())),
        (("", object(), None), ValueError("Cannot tuple-ize needs")),
        (("", [None], None), TypeError("All `needs` must be str")),
        (("", [()], None), TypeError("All `needs` must be str")),
        ## Check provides
        (("", "a", ()), ("", ("a",), ())),
        (("", "a", []), ("", ("a",), [])),
        (("", "a", object()), ValueError("Cannot tuple-ize provides")),
        (("", "a", (None,)), TypeError("All `provides` must be str")),
        (("", "a", [()]), TypeError("All `provides` must be str")),
    ],
)
def test_func_op_validation(opargs, exp):
    if isinstance(exp, Exception):
        with pytest.raises(type(exp), match=str(exp)):
            reparse_operation_data(*opargs)
    else:
        assert reparse_operation_data(*opargs)[:-1] == exp


@pytest.mark.parametrize(
    "args, kw, exp",
    [
        ((), {"node_props": []}, None),
        (
            (),
            {"node_props": 3.14},
            TypeError("node_props` must be a dict, was 'float':"),
        ),
        (
            (),
            {"node_props": "ab"},
            TypeError("node_props` must be a dict, was 'str':"),
        ),
    ],
)
def test_func_op_init(args, kw, exp):
    if isinstance(exp, Exception):
        with pytest.raises(type(exp), match=str(exp)):
            FnOp(str, "", *args, **kw)
    else:
        FnOp(str, "", *args, **kw)


@pytest.mark.parametrize(
    "result, dictres",
    [
        ({"aa": 1, "b": 2}, ...),
        (OrderedDict(aa=1, b=2), ...),
        (namedtuple("T", "a, bb")(1, 2), {"a": 1, "bb": 2}),
        (SimpleNamespace(a=1, bb=2), {"a": 1, "bb": 2}),
    ],
)
def test_returns_dict(result, dictres):
    if dictres is ...:
        dictres = result

    op = operation(lambda: result, provides=dictres.keys(), returns_dict=True)
    assert op.compute({}) == dictres

    op = operation(lambda: result, provides="a", returns_dict=False)
    assert op.compute({})["a"] == result


def test_returns_dict_extra():
    res = {"1": 1, "2": 2}
    op = operation(lambda: res, provides="1", returns_dict=True)
    assert op.compute({}) == {"1": 1}
    assert len(res) == 2  # check it did not mutate results


def test_returns_dict_keyword_renames():
    res = {"1": 1, "2": 2}
    op = operation(lambda: res, provides=keyword("11", "1"), returns_dict=True)
    assert op.compute({}) == {"11": 1}
    assert len(res) == 2  # check it did not mutate results

    res = {"1": 1, "11": 11}
    op = operation(lambda: res, provides=keyword("11", "1"), returns_dict=True)
    assert op.compute({}) == {"11": 1}  # original '11' was discarded
    assert len(res) == 2  # check it did not mutate results


@pytest.fixture(params=[None, ["a", "b"]])
def asked_outputs(request):
    return request.param


@pytest.mark.parametrize("result", [(), None, {}, {"a"}, "b", "ab", "abc", ""])
def test_results_sequence_1_provides_ok(result, asked_outputs):
    op = operation(lambda: result, provides=["a"])
    sol = op.compute({}, outputs=asked_outputs)
    assert sol["a"] == result


def test_results_sequence_lt_1_provides(asked_outputs):
    op = operation(lambda: NO_RESULT, provides=["a"])
    with pytest.raises(ValueError, match=f"Got -1 fewer results, while expected x1"):
        op.compute({}, outputs=asked_outputs)


@pytest.mark.parametrize(
    "result, nfewer", [((), -2), ({}, -2), (NO_RESULT, -2), ({"a"}, -1)]
)
def test_results_sequence_lt_many_provides(result, nfewer, asked_outputs):
    op = operation(lambda: result, provides=["a", "b"])
    with pytest.raises(
        ValueError, match=f"Got {nfewer} fewer results, while expected x2"
    ):

        op.compute({}, outputs=asked_outputs)


@pytest.mark.parametrize("result", ["", "a", "ab", "foobar", 3.14, None])
def test_results_validation_bad_iterable(result, asked_outputs):
    op = operation(lambda: result, provides=["a", "b"])
    with pytest.raises(TypeError, match=f"Expected x2 ITERABLE results, got"):
        op.compute({}, outputs=asked_outputs)


@pytest.mark.parametrize("result", [None, 3.14, [], "foo", ["b", "c", "e"], {"a", "b"}])
def test_dict_results_validation_BAD(result, asked_outputs):
    op = operation(lambda: result, provides=["a", "b"], returns_dict=True)
    with pytest.raises(ValueError, match="Expected results as mapping,"):
        op.compute({}, outputs=asked_outputs)


@pytest.mark.parametrize(
    "result, nmiss",
    [({}, 2), ({"a": 1}, 1), ({"a": 1, "c": 3}, 1), ({"aa": 1, "bb": 2}, 2)],
)
def test_dict_results_validation_MISMATCH(result, nmiss, asked_outputs):
    op = operation(lambda: result, provides=["a", "b"], returns_dict=True)
    with pytest.raises(ValueError, match=f"mismatched -{nmiss} provides"):
        op.compute({}, outputs=asked_outputs)


def test_varargs():
    def sumall(a, *args, b=0, **kwargs):
        return a + sum(args) + b + sum(kwargs.values())

    op = operation(
        sumall,
        name="t",
        needs=[
            "a",
            vararg("arg1"),
            vararg("arg2"),
            varargs("args"),
            optional("b"),
            optional("c"),
        ],
        provides="sum",
    )

    exp = sum(range(8))
    assert op.compute(dict(a=1, arg1=2, arg2=3, args=[4, 5], b=6, c=7))["sum"] == exp
    assert op.compute(dict(a=1, arg1=2, arg2=3, args=[4, 5], c=7))["sum"] == exp - 6
    assert op.compute(dict(a=1, arg1=2, arg2=3, args=[4, 5], b=6))["sum"] == exp - 7
    assert op.compute(dict(a=1, arg2=3, args=[4, 5], b=6, c=7))["sum"] == exp - 2
    assert op.compute(dict(a=1, arg1=2, arg2=3, b=6, c=7))["sum"] == exp - 4 - 5
    with pytest.raises(ValueError, match="Missing compulsory needs.+'a'"):
        assert op.compute(dict(arg1=2, arg2=3, b=6, c=7))


def test_op_node_props_bad():
    with pytest.raises(TypeError, match="`node_props` must be"):
        operation(lambda: None, name="a", node_props="SHOULD BE DICT")


def test_op_node_props():
    op_factory = operation(lambda: None, name="a", node_props=())
    assert op_factory.node_props == {}

    np = {"a": 1}
    op = operation(lambda: None, name="a", node_props=np)
    assert op.node_props == np


def _collect_op_props(pipe):
    return {
        k.name: v
        for k, v in pipe.net.graph.nodes.data(True)
        if isinstance(k, Operation)
    }


def test_pipeline_node_props():
    op1 = operation(lambda: None, name="a", node_props={"a": 11, "b": 0, "bb": 2})
    op2 = operation(lambda: None, name="b", node_props={"a": 3, "c": 4})
    pipeline = compose("n", op1, op2, node_props={"bb": 22, "c": 44})

    exp = {
        "a": {"typ": 1, "a": 11, "b": 0, "bb": 22, "c": 44},
        "b": {"typ": 1, "a": 3, "bb": 22, "c": 44},
    }
    node_props = _collect_op_props(pipeline)
    assert node_props == exp

    # Check node-prop sideffects are not modified
    #
    assert op1.node_props == {"a": 11, "b": 0, "bb": 2}
    assert op2.node_props == {"a": 3, "c": 4}


def test_pipeline_merge_node_props():
    op1 = operation(lambda: None, name="a", node_props={"a": 1})
    pipeline1 = compose("n1", op1)
    op2 = operation(lambda: None, name="a", node_props={"a": 11, "b": 0, "bb": 2})
    op3 = operation(lambda: None, name="b", node_props={"a": 3, "c": 4})
    pipeline2 = compose("n2", op2, op3)

    pipeline = compose(
        "n", pipeline1, pipeline2, node_props={"bb": 22, "c": 44}, nest=False
    )
    exp = {
        "a": {"typ": 1, "a": 1, "bb": 22, "c": 44},
        "b": {"typ": 1, "a": 3, "bb": 22, "c": 44},
    }
    node_props = _collect_op_props(pipeline)
    assert node_props == exp

    pipeline = compose(
        "n", pipeline1, pipeline2, node_props={"bb": 22, "c": 44}, nest=True
    )
    exp = {
        "n1.a": {"typ": 1, "a": 1, "bb": 22, "c": 44},
        "n2.a": {"typ": 1, "a": 11, "b": 0, "bb": 22, "c": 44},
        "n2.b": {"typ": 1, "a": 3, "bb": 22, "c": 44},
    }
    node_props = _collect_op_props(pipeline)
    assert node_props == exp


@pytest.mark.parametrize(
    "inp, exp",
    [
        ({"a": "b"}, {"a": "b"}.items()),
        ((1, 2), [(1, 2)]),
        ([(1, 2)], [(1, 2)]),
        ([], []),
        ((), []),
        (("ab", "ad"), [("a", "b"), ("a", "d")]),
    ],
)
def test_as_renames(inp, exp):
    as_renames((1, 2), "alias")


@pytest.mark.parametrize(
    "prov_aliases, ex",
    [
        (
            ((), {"a": 1}),
            TypeError(r"All `aliases` must be non-empty str, got: \[\('a', 1\)\]"),
        ),
        (
            ((), {"a": None}),
            TypeError(r"All `aliases` must be non-empty str, got: \[\('a', None\)\]"),
        ),
        (
            ((), {"a": ""}),
            TypeError(r"All `aliases` must be non-empty str, got: \[\('a', ''\)\]"),
        ),
        (
            ((), {"a": "A"}),
            ValueError(
                r"The `aliases` \['a'-->'A'\] rename non-existent provides in \[\]"
            ),
        ),
        (
            ("a", {"a": "A", "b": "B"}),
            ValueError(
                r"The `aliases` \['b'-->'B'\] rename non-existent provides in \['a'\]"
            ),
        ),
        (
            (sfx("a"), {sfx("a"): "a"}),
            ValueError("must not contain `sideffects"),
        ),
        (
            ("a", {"a": sfx("AA")}),
            ValueError("must not contain `sideffects"),
        ),
        (
            (["a", "b"], {"a": "b"}),
            ValueError(r"clash with existing provides in \['a', 'b'\]"),
        ),
        ## Implicits
        #
        (
            ([implicit("i")], {implicit("i"): "II"}),
            ValueError("must not contain `implicits"),
        ),
        (
            (["i"], {"i": implicit("II")}),
            ValueError("must not contain `implicits"),
        ),
    ],
)
def test_func_op_validation_aliases_BAD(prov_aliases, ex):
    with pytest.raises(type(ex), match=str(ex)):
        reparse_operation_data("t", None, *prov_aliases)


def test_keyword_jsonp():
    op = operation(lambda *, bar: bar * 2, "kw", needs=keyword("foo/bar"), provides="a")
    sol = op.compute({"foo/bar": "ciao"})
    assert sol == {"a": "ciaociao"}


def test_cwd_fnop():
    op = operation(
        str,
        None,
        needs=[
            "a",
            "a/b",
            "/r/b",
            optional("o"),
            keyword("k"),
            implicit("i"),
            vararg("v1"),
            varargs("v2"),
            sfx("s1"),
            sfxed("s2", "s22"),
            vcat("vc"),
        ],
        provides=["A/B", "C", "/R"],
        aliases=[("A/B", "aa"), ("C", "CC"), ("/R", "RR")],
        cwd="root",
    )
    exp = """
    FnOp(name='str',
        needs=['root/a'($),
            'root/a/b'($),
            '/r/b'($),
            'root/o'($?'o'),
            'root/k'($>'k'),
            'root/i'($),
            'root/v1'($*),
            'root/v2'($+),
            sfx('s1'),
            sfxed('root/s2'($),
            's22'),
            'root/vc'($)],
        provides=['root/A/B'($),
            'root/C'($),
            '/R'($),
            'root/aa'($),
            'root/CC'($),
            'root/RR'($)],
         aliases=[('root/A/B'($), 'root/aa'($)),
            ('root/C'($), 'root/CC'($)),
            ('/R'($), 'root/RR'($))],
        fn='str')
    """
    assert oneliner(op) == oneliner(exp)


def test_cwd_pipeline():
    op = compose(
        ...,
        operation(
            str,
            None,
            needs=[
                "a",
                "a/b",
                "/r/b",
            ],
            provides=["A/B", "C", "/R"],
            aliases=[("A/B", "aa"), ("C", "CC"), ("/R", "RR")],
        ),
        cwd="/root",
    )
    exp = """
    Pipeline('test_cwd_pipeline',
        needs=['/root/a'($),
            '/root/a/b'($),
            '/r/b'($)],
        provides=['/root/A/B'($),
            '/root/C'($),
            '/R'($),
            '/root/aa'($),
            '/root/CC'($),
            '/root/RR'($)],
        x1 ops: str)
    """
    assert oneliner(op) == oneliner(exp)


@pytest.mark.parametrize(
    "provide, aliases, exp",
    [
        ("a", {"a": "aa"}, {"a": "k", "aa": "k"}),
        (
            sfxed("a", "1"),
            {sfxed("a", "1"): "aa"},
            {"a": "k", "aa": "k"},
        ),
        (
            "a",
            {"a": sfxed("a", "1")},
            {"a": "k"},
        ),
        (
            sfxed("a", "1"),
            {sfxed("a", "1"): sfxed("b", "1")},
            {"a": "k", "b": "k"},
        ),
    ],
)
def test_provides_aliases(provide, aliases, exp):
    op = operation(str, name="t", needs="s", provides=provide, aliases=aliases)
    assert op.provides == aliases.keys() | aliases.values()
    assert op.compute({"s": "k"}) == exp


def test_sfxed_needs_in_pipeline():
    deps = (sfxed("a", "A", "B"), sfxed("a", "A", "C"), "c", "c")
    op = operation(str, "hh", needs=deps)

    singularized = (sfxed("a", "A"), sfxed("a", "B"), sfxed("a", "C"), "c")
    assert op.needs == singularized
    assert op._user_needs == deps
    assert op._fn_needs == ("a", "c", "c")

    pipe = compose(..., op)
    assert pipe.needs == singularized


def test_sfxed_provides_in_pipeline():
    deps = (sfxed("a", "A", "B"), sfxed("a", "A", "C"), "c", "c")
    op = operation(str, "hh", provides=deps)

    singularized = (sfxed("a", "A"), sfxed("a", "B"), sfxed("a", "C"), "c")
    assert op.provides == singularized
    assert op._user_provides == deps
    assert op._fn_provides == ("a", "c", "c")

    pipe = compose(..., op)
    assert pipe.provides == singularized


@pytest.mark.parametrize("rescheduled", [0, 1])
def test_reschedule_more_outs(rescheduled, caplog):
    op = operation(
        lambda: [1, 2, 3], name="t", provides=["a", "b"], rescheduled=rescheduled
    )
    op.compute({})
    assert "+1 more results, while expected x2" in caplog.text


def test_reschedule_unknown_dict_outs(caplog):
    op = operation(
        lambda: {"b": "B"}, name="t", provides=["a"], rescheduled=1, returns_dict=1
    )
    caplog.set_level(logging.INFO)
    op.compute({})
    assert "contained +1 unknown provides['b']" in caplog.text

    caplog.clear()
    op = operation(
        lambda: {"a": 1, "BAD": "B"},
        name="t",
        provides=["a"],
        rescheduled=1,
        returns_dict=1,
    )
    op.compute({})
    assert "contained +1 unknown provides['BAD']" in caplog.text


def test_rescheduled_op_repr():
    op = operation(str, name="t", provides=["a"], rescheduled=True)
    assert str(op) == "FnOp?(name='t', provides=['a'], fn='str')"


def test_endured_op_repr():
    op = operation(str, name="t", provides=["a"], endured=True)
    assert str(op) == "FnOp!(name='t', provides=['a'], fn='str')"


def test_endured_rescheduled_op_repr():
    op = operation(str, name="t", rescheduled=1, endured=1)
    assert str(op) == "FnOp!?(name='t', fn='str')"


def test_parallel_op_repr():
    op = operation(str, name="t", provides=["a"], parallel=True)
    assert str(op) == "FnOp|(name='t', provides=['a'], fn='str')"


def test_marshalled_op_repr():
    op = operation(str, name="t", provides=["a"], marshalled=True)
    assert str(op) == ("FnOp&(name='t', provides=['a'], fn='str')")


def test_marshalled_parallel_op_repr():
    op = operation(str, name="t", parallel=1, marshalled=1)
    assert str(op) == "FnOp|&(name='t', fn='str')"


def test_ALL_op_repr():
    op = operation(str, name="t", rescheduled=1, endured=1, parallel=1, marshalled=1)
    assert str(op) == "FnOp!?|&(name='t', fn='str')"


def test_CONFIG_op_repr():
    with operations_endured(1), operations_reschedullled(1), tasks_in_parallel(
        1
    ), tasks_marshalled(1):
        op = operation(str, name="t")
        assert str(op) == "FnOp!?|&(name='t', fn='str')"
    op = operation(str, name="t", rescheduled=0, endured=0, parallel=0, marshalled=0)
    assert str(op) == "FnOp(name='t', fn='str')"


def test_reschedule_outputs():
    op = operation(
        lambda: ["A", "B"], name="t", provides=["a", "b", "c"], rescheduled=True
    )
    assert op.compute({}) == {"a": "A", "b": "B"}

    # NOTE that for a single return item, it must be a collection.
    op = operation(lambda: ["AA"], name="t", provides=["a", "b"], rescheduled=True)
    assert op.compute({}) == {"a": "AA"}

    op = operation(lambda: NO_RESULT, name="t", provides=["a", "b"], rescheduled=True)
    assert op.compute({}) == {}
    op = operation(
        lambda: NO_RESULT_BUT_SFX, name="t", provides=["a", "b"], rescheduled=True
    )
    assert op.compute({}) == {}

    op = operation(
        lambda: {"b": "B"}, name="t", provides=["a", "b"], rescheduled=1, returns_dict=1
    )
    assert op.compute({}) == {"b": "B"}

    op = operation(
        lambda: {"b": "B"},
        name="t",
        provides=["a", "b"],
        aliases={"a": "aa", "b": "bb"},
        rescheduled=1,
        returns_dict=1,
    )
    assert op.compute({}) == {"b": "B", "bb": "B"}


@pytest.mark.parametrize("attr, value", [("outputs", [1]), ("predicate", lambda: None)])
def test_pipeline_narrow_attributes(attr, value):
    pipeline = compose("1", operation(str, name="op1"))
    assert getattr(pipeline.withset(**{attr: value}), attr) == value


_attr_values = [
    ("rescheduled", None),
    ("rescheduled", 1),
    ("rescheduled", False),
    ("endured", None),
    ("endured", True),
    ("endured", 0),
    ("parallel", None),
    ("parallel", True),
    ("parallel", 0),
    ("marshalled", None),
    ("marshalled", True),
    ("marshalled", 0),
]


@pytest.mark.parametrize("attr, value", _attr_values)
def test_op_withset_conveys_attr(attr, value):
    kw = {attr: value}
    op1 = operation(str)
    assert getattr(op1, attr) is None

    op2 = op1.withset(**kw)
    assert getattr(op2, attr) == value
    assert getattr(op1, attr) is None

    op3 = op2.withset()
    assert getattr(op3, attr) == value


@pytest.mark.parametrize("attr, value", _attr_values)
def test_pipeline_conveys_attr_to_ops(attr, value):
    def _opsattrs(ops, attr, value):
        vals = [getattr(op, attr) for op in ops if isinstance(op, Operation)]
        assert all(v == value for v in vals)

    kw = {attr: value}
    _opsattrs(compose("1", operation(str), **kw).net.graph, attr, value)
    _opsattrs(
        compose(
            "2", operation(str, name="1"), operation(str, name="2"), **kw
        ).net.graph,
        attr,
        value,
    )


@pytest.mark.parametrize(
    "op_fact",
    [
        lambda: Operation,
        lambda: FnOp,
        lambda: operation(str),
        lambda: operation(lambda: None),
    ],
)
def test_serialize_op(op_fact, ser_method):
    op = op_fact()
    if "pickle" in str(ser_method) and "lambda" in str(getattr(op, "fn", ())):
        with pytest.raises(AttributeError, match="^Can't pickle local object"):
            ser_method(op) == op
        raise pytest.xfail(reason="Pickling fails for locals i.e. lambas")

    assert ser_method(op) == op


def test_serialize_pipeline(samplenet, ser_method):
    def eq(pipe1, pipe2):
        return pipe1.name == pipe2.name and pipe1.ops == pipe2.ops

    assert eq(ser_method(samplenet), samplenet)


def test_non_op_given():
    with pytest.raises(
        TypeError, match=r"(?s)Received x1 non-Operation instances: \[1\]"
    ):
        compose("", operation(None, name="b"), 1, operation(None, name="a"))
    with pytest.raises(
        TypeError,
        match=r"(?s)Received x2 non-Operation instances: \['noop', <function .+>\]",
    ):
        compose("", "noop", operation(None, name="b"), lambda: None)


def test_op_rename():
    op = operation(
        str,
        name="op1",
        needs=sfx("a"),
        provides=["a", sfx("b")],
        aliases=[("a", "b")],
    )

    def renamer(na):
        assert na.op
        assert not na.parent
        return dep_renamed(na.name, lambda name: f"PP.{name}")

    ren = op.withset(renamer=renamer)
    got = str(ren)
    assert got == (
        """
    FnOp(name='PP.op1', needs=[sfx('PP.a')], provides=['PP.a', sfx('PP.b'), 'PP.b'], aliases=[('PP.a', 'PP.b')], fn='str')
        """.strip()
    )


def test_op_rename_parts():
    op = operation(
        str,
        name="op1",
        needs=[sfx("a/b"), "/a/b"],
        provides=["b/c", sfxed("d/e/f", "k/l")],
        aliases=[("b/c", "/b/t")],
    )

    def renamer(na):
        if na.name and na.typ.endswith(".jsonpart"):
            return f"PP.{na.name}"

    ren = op.withset(renamer=renamer)
    got = str(ren)
    print(got)
    assert got == oneliner(
        """
        FnOp(name='op1',
            needs=[sfx('a/b'), '/PP.a/PP.b'($)],
            provides=['PP.b/PP.c'($), sfxed('PP.d/PP.e/PP.f'($), 'k/l'), '/PP.b/PP.t'($)],
            aliases=[('PP.b/PP.c'($), '/PP.b/PP.t'($))], fn='str')
        """,
    )


def test_pipe_rename():
    pipe = compose(
        "t",
        operation(str, name="op1", needs=sfx("a")),
        operation(
            str,
            name="op2",
            needs=sfx("a"),
            provides=["a", sfx("b")],
            aliases=[("a", "b")],
        ),
    )

    def renamer(na):
        assert na.op
        assert not na.parent
        return dep_renamed(na.name, lambda name: f"PP.{name}")

    ren = pipe.withset(renamer=renamer)
    got = str(ren)
    assert got == (
        """
    Pipeline('t', needs=[sfx('PP.a')], provides=['PP.a', sfx('PP.b'), 'PP.b'], x2 ops: PP.op1, PP.op2)
        """.strip()
    )
    got = str(ren.ops)
    assert got == oneliner(
        """
        [FnOp(name='PP.op1', needs=[sfx('PP.a')], fn='str'),
         FnOp(name='PP.op2', needs=[sfx('PP.a')], provides=['PP.a', sfx('PP.b'), 'PP.b'],
         aliases=[('PP.a', 'PP.b')], fn='str')]
        """
    )

    ## Check dictionary with callables
    #
    ren = pipe.withset(
        renamer={
            "op1": lambda n: "OP1",
            "op2": False,
            "a": optional("a"),
            "b": "B",
        }
    )
    got = str(ren.ops)
    assert got == oneliner(
        """
        [FnOp(name='OP1', needs=[sfx('a')], fn='str'),
         FnOp(name='op2', needs=[sfx('a')], provides=['a'(?), sfx('b'), 'B'],
         aliases=[('a'(?), 'B')], fn='str')]
        """
    )


def test_conveyor_identity_fn():
    op = operation(name="copy values", needs="a")()
    assert not op.fn
    op = operation(None, needs="a", provides="A")
    assert not op.fn

    op = operation(None, name="a", needs="a", provides="A")
    assert op.fn
    assert op(a=5) == {"A": 5}

    op = operation(name="a", needs=["a", "b"], provides=["A", "B"])()
    assert op.compute({"a": 5, "b": 6}) == {"A": 5, "B": 6}

    op = operation(name="a", needs=["a", keyword("b")], provides=["A", "B"])()
    assert op(a=55, b=66) == {"A": 55, "B": 66}

    op = operation(
        fn=None,
        name="a",
        needs=[optional("a"), vararg("b"), "c"],
        # positional, vararg, keyword, optional
        provides=["C", "B", "A"],
    )
    assert op(c=7, a=5, b=6) == {"A": 5, "B": 6, "C": 7}

    # TODO: when `varargs` work for Outputs.
    # op = operation(
    #     name="a", needs=[sfxed("a", 's'), optional=1), sfxed_varargs("b", 's'), "c"],
    #     # vararg, keyword, optional
    #     provides=["C", "B", "A", varargs(sadasa"b", 's')]
    # )()
    # assert op(c=7, a=5, b=[6]) == {"A": 5, "B1": [6], "B2", "C": 7}


def test_pandas_result():
    ser = pd.Series([1, 2])
    sol = operation(lambda: ser, name="pandas", provides="a").compute()
    assert (sol["a"] == ser).all()


def test_pandas_input():
    ser = pd.Series([1, 2])
    sol = operation(fn=None, name="pandas", needs="a", provides="A")(a=ser)
    assert (sol["A"] == ser).all()
    sol = operation(fn=None, name="pandas", needs="a", provides="A").compute({"a": ser})
    assert (sol["A"] == ser).all()
