# Copyright 2016, Yahoo Inc.
# Licensed under the terms of the Apache License, Version 2.0. See the LICENSE file associated with the project for terms.
"""
:term:`modifier`\\s (print-out with :term:`diacritic`\\s) change :term:`dependency` behavior during :term:`planning` & :term:`execution`.

The `needs` and `provides` annotated with *modifiers* designate, for instance,
:term:`optional <optionals>` function arguments, or "ghost" :term:`sideffects`.

.. note::
    This module (along with :mod:`.op` & :mod:`.pipeline`) is what client code needs
    to define pipelines *on import time* without incurring a heavy price
    (~7ms on a 2019 fast PC)

**Diacritics**

.. diacritics-start

The :meth:`representation <._Modifier.__repr__>` of modifier-annotated dependencies
utilize a combination of these **diacritics**:

.. parsed-literal::

    >   : :func:`.keyword`
    ?   : :func:`.optional`
    *   : :func:`.vararg`
    +   : :func:`.varargs`
    $   : :term:`accessor` (mostly for :term:`jsonp`)

.. diacritics-end
"""
import enum
from functools import lru_cache, partial
import operator
from typing import (
    Any,
    Callable,
    Collection,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Union,
)

# fmt: off
#: Arguments-presence patterns for :class:`_Modifier` constructor.
#: Combinations missing raise errors.
_modifier_cstor_matrix = {
# TODO: Add `implicit` in the table, to augment REPR & forbid implicit sfxed.
# (7, kw, opt, accessors, sfxed, sfx): (STR, REPR, FUNC) OR None
700000: None,
710000: (       "%(dep)s",                  "'%(dep)s'(%(acs)s>%(kw)s)",    "keyword"),
711000: (       "%(dep)s",                  "'%(dep)s'(%(acs)s?%(kw)s)",    "optional"),
702000: (       "%(dep)s",                  "'%(dep)s'(*)",                 "vararg"),
703000: (       "%(dep)s",                  "'%(dep)s'(+)",                 "varargs"),
# Accessor
700100: (       "%(dep)s",                  "'%(dep)s'($)",                 "accessor"),
710100: (       "%(dep)s",                  "'%(dep)s'($>%(kw)s)",          "keyword"),
711100: (       "%(dep)s",                  "'%(dep)s'($?%(kw)s)",          "optional"),
702100: (       "%(dep)s",                  "'%(dep)s'($*)",                "vararg"),
703100: (       "%(dep)s",                  "'%(dep)s'($+)",                "varargs"),

700010: (  "sfx('%(dep)s')",            "sfx('%(dep)s')",    "sfx"),
701010: (  "sfx('%(dep)s')",            "sfx('%(dep)s'(?))", "sfx"),
#SFXED
700011: ("sfxed('%(dep)s', %(sfx)s)", "sfxed(%(acs)s'%(dep)s', %(sfx)s)",           "sfxed"),
710011: ("sfxed('%(dep)s', %(sfx)s)", "sfxed(%(acs)s'%(dep)s'(>%(kw)s), %(sfx)s)",  "sfxed"),
711011: ("sfxed('%(dep)s', %(sfx)s)", "sfxed(%(acs)s'%(dep)s'(?%(kw)s), %(sfx)s)",  "sfxed"),
702011: ("sfxed('%(dep)s', %(sfx)s)", "sfxed(%(acs)s'%(dep)s'(*), %(sfx)s)",        "sfxed_vararg"),
703011: ("sfxed('%(dep)s', %(sfx)s)", "sfxed(%(acs)s'%(dep)s'(+), %(sfx)s)",        "sfxed_varargs"),
# Accessor
700111: ("sfxed('%(dep)s', %(sfx)s)", "sfxed('%(dep)s'($), %(sfx)s)",               "sfxed"),
710111: ("sfxed('%(dep)s', %(sfx)s)", "sfxed('%(dep)s'($>%(kw)s), %(sfx)s)",        "sfxed"),
711111: ("sfxed('%(dep)s', %(sfx)s)", "sfxed('%(dep)s'($?%(kw)s), %(sfx)s)",        "sfxed"),
702111: ("sfxed('%(dep)s', %(sfx)s)", "sfxed('%(dep)s'($*), %(sfx)s)",              "sfxed_vararg"),
703111: ("sfxed('%(dep)s', %(sfx)s)", "sfxed('%(dep)s'($+), %(sfx)s)",              "sfxed_varargs"),
}
# fmt: on


def _match_modifier_args(name, *args):
    flags = [int(bool(i)) for i in args]

    # expand optional
    if args[1]:
        flags[1] = args[1].value
    pattern = "".join(str(i) for i in flags)
    pattern = int(f"7{pattern}")
    if pattern not in _modifier_cstor_matrix:
        raise ValueError(f"Invalid modifier arguments: {name}, {args}, {pattern}")

    return _modifier_cstor_matrix[pattern]


class _Optionals(enum.Enum):
    keyword = 1
    vararg = 2
    varargs = 3


class Accessor(NamedTuple):
    """
    Getter/setter functions to extract/populate values from a :term:`solution layer`.

    .. Note::
        Don't use its attributes directly, prefer instead the functions returned
        from :func:`.acc_contains()` etc on any dep (plain strings included).

    TODO: drop accessors, push functionality into :term:`jsonp` alone.
    """

    #: the containment checker, like: ``dep in sol``;
    contains: Callable[[dict, str], Any]
    #: the getter, like: ``getitem(sol, dep) -> value``
    getitem: Callable[[dict, str], Any]
    #: the setter, like: ``setitem(sol, dep, val)``,
    setitem: Callable[[dict, str, Any], None]
    #: the deleter, like: ``delitem(sol, dep)``
    delitem: Callable[[dict, str], None]
    #: mass updater, like: ``update(sol, item_values)``,
    update: Callable[[dict, Collection[Tuple[str, Any]]], None] = None

    def validate(self):
        """Call me early to fail asap (if it must); returns self instance. """
        oks = [callable(i) for i in self]
        oks[-1] |= self[-1] is None  # `update` can be None
        if not all(oks):
            errs = dict(pair for pair, ok in zip(self._asdict().items(), oks) if not ok)
            raise TypeError(
                f"Accessor's {list(errs)} must be callable, were: {list(errs.values())}"
            )
        return self


@lru_cache()
def JsonpAcc():
    """Read/write `jsonp` paths found on modifier's "extra' attribute `jsonpath` """
    from . import jsonpointer as jsp

    return Accessor(
        contains=jsp.contains_path,
        getitem=jsp.resolve_path,
        setitem=jsp.set_path_value,
        delitem=jsp.pop_path,
        update=jsp.update_paths,
    )


@lru_cache()
def VCatAcc():
    """Read/write `jsonp` and concat columns (axis=1) if both doc & value are Pandas. """
    from . import jsonpointer as jsp

    return Accessor(
        contains=jsp.contains_path,
        getitem=jsp.resolve_path,
        setitem=partial(jsp.set_path_value, concat_axis=0),
        delitem=jsp.pop_path,
        update=partial(jsp.update_paths, concat_axis=0),
    )


@lru_cache()
def HCatAcc():
    """Read/write `jsonp` and concat columns (axis=1) if both doc & value are Pandas. """
    from . import jsonpointer as jsp

    return Accessor(
        contains=jsp.contains_path,
        getitem=jsp.resolve_path,
        setitem=partial(jsp.set_path_value, concat_axis=1),
        delitem=jsp.pop_path,
        update=partial(jsp.update_paths, concat_axis=1),
    )


class _Modifier(str):
    """
    Annotate a :term:`dependency` with a combination of :term:`modifier`.

    This class is private, because client code should not need to call its cstor,
    or check if a dependency ``isinstance()``, but use these facilities instead:

    - the *factory* functions like :func:`.keyword`, :func:`optional` etc,
    - the *predicates* like :func:`is_optional()`, :func:`is_pure_sfx()` etc,
    - the *conversion* functions like :func:`dep_renamed()`, :func:`dep_stripped()` etc,
    - and only *rarely* (and with care) call its :meth:`modifier_withset()` method or
      :func:`_modifier()` factor functions.

    :param kw:
        any extra attributes not needed by execution machinery
        such as the ``jsonpath``, which is used only by :term:`accessor`.

    .. Note::
        Factory function:func:`_modifier()` may return a plain string, if no other
        arg but ``name`` is given.
    """

    #: pre-calculated representation
    _repr: str
    #: The name of a modifier function here, needed to reconstruct
    #: cstor code in :meth:`.cmd()`
    _func: str
    #: Map my name in `needs` into this kw-argument of the function.
    #: :func:`get_keyword()` returns it.
    _keyword: str = None
    #: required is None, regular optional or varargish?
    #: :func:`is_optional()` returns it.
    #: All regulars are `keyword`.
    _optional: _Optionals = None
    #: An :term:`accessor` with getter/setter functions to read/write solution values.
    #: Any sequence of 2-callables will do.
    _accessor: Accessor = None
    #: Has value only for sideffects: the pure-sideffect string or
    #: the existing :term:`sideffected` dependency.
    _sideffected: str = None
    #: At least one name(s) denoting the :term:`sideffects` modification(s) on
    #: the :term:`sideffected`, performed/required by the operation.
    #:
    #: - If it is an empty tuple`, it is an abstract sideffect,
    #:    and :func:`is_pure_optional()` returns True.
    #: - If not empty :func:`is_sfxed()` returns true
    #:   (the :attr:`._sideffected`).
    _sfx_list: Tuple[Union[str, None]] = ()

    def __new__(
        cls,
        name,
        _repr,
        _func,
        keyword,
        optional: _Optionals,
        accessor,
        sideffected,
        sfx_list,
        **kw,
    ) -> "_Modifier":
        """Warning, returns None! """
        ## sanity checks & preprocessing
        #
        if optional is not None and not isinstance(optional, _Optionals):
            raise ValueError(
                f"Invalid _Optional enum {optional!r}\n  locals={locals()}"
            )
        if accessor:
            if not isinstance(accessor, Accessor):
                accessor = Accessor(*(not isinstance(accessor, str) and accessor))
            accessor.validate()
        if sideffected and is_sfx(sideffected):
            raise ValueError(
                f"`sideffected` cannot be `sfx`, got {sideffected!r}"
                f"\n  locals={locals()}"
            )

        # TODO: Add `implicit` in the table, to augment REPR & forbid implicit sfxed.
        if sideffected and kw.get("_implicit"):
            raise ValueError(
                f"`sideffected` cannot be `implicit`, got {sideffected!r}"
                f"\n  locals={locals()}"
            )
        double_sideffects = [
            f"{type(i).__name__}({i!r})" for i in sfx_list if is_sfx(i)
        ]
        if double_sideffects:
            raise ValueError(
                f"`sfx_list` cannot contain sideffects, got {double_sideffects!r}"
                f"\n  locals={locals()}"
            )

        obj = super().__new__(cls, name)
        obj._repr = _repr
        obj._func = _func
        if keyword:
            obj._keyword = keyword
        if optional:
            obj._optional = optional
        if accessor:
            obj._accessor = accessor
        if sideffected:
            obj._sideffected = sideffected
        if sfx_list:
            obj._sfx_list = sfx_list
        vars(obj).update(kw)
        return obj

    def __repr__(self):
        """Note that modifiers have different ``repr()`` from ``str()``."""
        return self._repr

    @property
    def cmd(self):
        """the code to reproduce it"""
        dep = self._sideffected or str(self)
        items = [f"'{dep}'"]
        if self._sfx_list:
            items.append(", ".join(f"'{i}'" for i in self._sfx_list))
        if self._keyword and self._keyword != dep:
            keyword = f"'{self._keyword}'"
            items.append(f"keyword={keyword}" if self._sfx_list else keyword)
        if self._optional == _Optionals.keyword and self._func != "optional":
            items.append("optional=1" if self._sfx_list else "1")
        if self._accessor:
            items.append(f"accessor={self._accessor!r}")
        return f"{self._func}({', '.join(items)})"

    def __getnewargs__(self):
        return (
            str(self),
            self._repr,
            self._func,
            self._keyword,
            self._optional,
            self._accessor,
            self._sideffected,
            self._sfx_list,
        )


def _modifier(
    name,
    *,
    keyword=None,
    optional: _Optionals = None,
    accessor=None,
    sideffected=None,
    sfx_list=(),
    jsonp=None,
    **kw,
) -> Union[str, _Modifier]:
    """
    A :class:`_Modifier` factory that may return a plain str when no other args given.

    It decides the final `name` and `_repr` for the new modifier by matching
    the given inputs with the :data:`_modifier_cstor_matrix`.

    :param kw:
        extra kv pairs assigned as :class:`_Modifier` **private** attributes
        (prefixed with ``_`` if not already) only if values are not null.
        Here used for :term:`implicit`, and client code may extend its own modifiers.
    """
    if jsonp is not None:
        if isinstance(jsonp, str):
            from .jsonpointer import jsonp_path

            jsonp = jsonp_path(jsonp)
        kw["_jsonp"] = jsonp  # WARN: must be False or a collection for jsonp-accessors!
    # Prevent sfx-jsonp.
    elif "/" in name and jsonp is None and (sideffected is None or sfx_list):
        from .jsonpointer import jsonp_path

        kw["_jsonp"] = jsonp_path(name)
    # Don't override user's accessor.
    #
    if not accessor and kw.get("_jsonp"):
        accessor = JsonpAcc()

    args = (name, keyword, optional, accessor, sideffected, sfx_list)
    formats = _match_modifier_args(*args)

    ## Private-ize all keywords and throw away nulls.
    kw = {
        k if k.startswith("_") else f"_{k}": v for k, v in kw.items() if v is not None
    }
    if not formats:
        if kw:
            # Just jsonp given.
            assert not accessor and (optional, accessor, sideffected, sfx_list) == (
                None,
                None,
                None,
                (),
            ), locals()
            return _Modifier(name, name, "modify", *args[1:], **kw)

        # Make a plain string instead.
        return str(name)

    str_fmt, repr_fmt, func = formats
    fmt_args = {
        "dep": name,
        "kw": f"'{keyword}'" if keyword != name else "",
        "sfx": ", ".join(f"'{i}'" for i in sfx_list),
        "acs": "$" if accessor else "",
    }
    _repr = repr_fmt % fmt_args
    name = str_fmt % fmt_args

    return _Modifier(name, _repr, func, *args[1:], **kw)


def modifier_withset(
    dep,
    name=...,
    keyword=...,
    optional: _Optionals = ...,
    accessor=...,
    sideffected=...,
    sfx_list=...,
    **kw,
) -> Union["_Modifier", str]:
    """
    Make a new modifier with changes -- handle with care.

    :return:
        Delegates to :func:`_modifier`, so returns a plain string if no args left.
    """
    if isinstance(dep, _Modifier):
        kw = {
            **{
                k.lstrip("_"): v
                for k, v in vars(dep).items()
                # Regenerate cached, truthy-only, jsonp-parts.
                if k != "_jsonp" or not v
            },
            **{k: v for k, v in locals().items() if v is not ...},
            **kw,
        }
        kw = {
            k: v
            for k, v in kw.items()
            if k not in set(["dep", "name", "kw", "repr", "func"])
        }
        if name is ...:
            name = dep._sideffected or str(dep)
    else:
        if name is ...:
            name = dep

    return _modifier(name=name, **kw)


def get_keyword(dep) -> Optional[str]:
    """
    Check if a :term:`dependency` is keyword (and get it, last step if `jsonp`).

    All non-varargish optionals are "keyword" (including sideffected ones).

    :return:
        the :attr:`._keyword`
    """
    return getattr(dep, "_keyword", None)


def is_optional(dep) -> Optional[_Optionals]:
    """
    Check if a :term:`dependency` is optional.

    Varargish & optional sideffects are included.

    :return:
        the :attr:`._optional`
    """
    return getattr(dep, "_optional", None)


def is_vararg(dep) -> bool:
    """Check if an :term:`optionals` dependency is `vararg`."""
    return getattr(dep, "_optional", None) == _Optionals.vararg


def is_varargs(dep) -> bool:
    """Check if an :term:`optionals` dependency is `varargs`."""
    return getattr(dep, "_optional", None) == _Optionals.varargs


def is_varargish(dep) -> bool:
    """Check if an :term:`optionals` dependency is :term:`varargish`."""
    return dep._optional in (_Optionals.vararg, _Optionals.vararg)


def jsonp_ize(dep):
    """Parse dep as :term:`jsonp` (unless modified with ``jsnop=False``) or is pure sfx. """
    return modify(dep) if "/" in dep and type(dep) is str else dep  # sfxed-deps already


def get_jsonp(dep) -> Union[List[str], None]:
    """Check if dependency is :term:`json pointer path` and return its steps."""
    return getattr(jsonp_ize(dep), "_jsonp", None)


def is_sfx(dep) -> Optional[str]:
    """
    Check if a dependency is :term:`sideffects` or :term:`sideffected`.

    :return:
        the :attr:`._sideffected`
    """
    return getattr(dep, "_sideffected", None)


def is_pure_sfx(dep) -> bool:
    """Check if it is :term:`sideffects` but not a :term:`sideffected`."""
    return getattr(dep, "_sideffected", None) and not getattr(dep, "_sfx_list", None)


def is_sfxed(dep) -> bool:
    """
    Check if it is :term:`sideffected`.

    :return:
        the :attr:`._sfx_list` if it is  a *sideffected* dep, None/empty-tuple otherwise
    """
    return getattr(dep, "_sideffected", None) and getattr(dep, "_sfx_list", None)


def is_implicit(dep) -> bool:
    """Return if it is a :term:`implicit` dependency. """
    return getattr(dep, "_implicit", None)


def get_accessor(dep) -> bool:
    """
    Check if dependency has an :term:`accessor`, and get it (if funcs below are unfit)

    :return:
        the :attr:`._accessor`
    """
    return getattr(dep, "_accessor", None)


def acc_contains(dep) -> Callable[[Collection, str], Any]:
    """
    A fn like :func:`operator.contains` for any `dep` (with-or-without :term:`accessor`)
    """
    acc = getattr(dep, "_accessor", None)
    return acc.contains if acc else operator.contains


def acc_getitem(dep) -> Callable[[Collection, str], Any]:
    """
    A fn like :func:`operator.getitem` for any `dep` (with-or-without :term:`accessor`)
    """
    acc = getattr(dep, "_accessor", None)
    return acc.getitem if acc else operator.getitem


def acc_setitem(dep) -> Callable[[Collection, str, Any], None]:
    """
    A fn like :func:`operator.setitem` for any `dep` (with-or-without :term:`accessor`)
    """
    acc = getattr(dep, "_accessor", None)
    return acc.setitem if acc else operator.setitem


def acc_delitem(dep) -> Callable[[Collection, str], None]:
    """
    A fn like :func:`operator.delitem` for any `dep` (with-or-without :term:`accessor`)
    """
    acc = getattr(dep, "_accessor", None)
    return acc.delitem if acc else operator.delitem


def dependency(dep) -> str:
    """
    Returns the underlying dependency name (just str)

    For non-sideffects, it coincides with str(), otherwise,
    the the pure-sideffect string or the existing :term:`sideffected` dependency
    stored in :attr:`._sideffected`.
    """
    return str(dep) if is_sfx(dep) else dep._sideffected


def dep_renamed(dep, ren, jsonp=None) -> Union[_Modifier, str]:
    """
    Renames `dep` as `ren` or call `ren`` (if callable) to decide its name,

    preserving any :func:`keyword` to old-name.

    :param jsonp:
        None (derrived from `name`), ``False``, str, collection of str/callable (last one)
        See generic :func:`.modify` modifier.

    For :term:`sideffected` it renames the dependency (not the *sfx-list*) --
    you have to do it that manually with a custom renamer-function, if ever
    the need arise.
    """
    if callable(ren):
        renamer = ren
    else:
        renamer = lambda n: ren

    if isinstance(dep, _Modifier) or jsonp is not None:
        if is_sfx(dep):
            new_name = renamer(dep._sideffected)
            dep = modifier_withset(
                dep, name=new_name, sideffected=new_name, jsonp=jsonp
            )
        else:
            dep = modifier_withset(dep, name=renamer(str(dep)), jsonp=jsonp)
    else:  # plain string
        dep = renamer(dep)

    return dep


def dep_singularized(dep) -> Iterable[Union[str, _Modifier]]:
    """
    Return one sideffected for each sfx in :attr:`._sfx_list`, or iterate `dep` in other cases.
    """
    sfx_list = is_sfxed(dep)
    return (
        [modifier_withset(dep, sfx_list=(s,)) for s in sfx_list] if sfx_list else (dep,)
    )


def dep_stripped(dep) -> Union[str, _Modifier]:
    """
    Return the :attr:`._sideffected` if `dep` is :term:`sideffected`, `dep` otherwise,

    conveying all other properties of the original modifier to the stripped dependency.
    """
    if is_sfxed(dep):
        dep = modifier_withset(
            dep, name=dep._sideffected, sideffected=None, sfx_list=()
        )
    return dep


############
## Announced API
## (exported with "*" in package.__init___)
##


def modify(
    name: str, *, keyword=None, jsonp=None, implicit=None, accessor: Accessor = None
) -> _Modifier:
    """
    Generic :term:`modifier` for term:`json pointer path` & :term:`implicit` dependencies.

    :param jsonp:
        If given, it may be some other json-pointer expression, or
        the pre-splitted *parts* of the :term:`jsonp` dependency -- in that case,
        the dependency name is irrelevant -- or a falsy (but not ``None``) value,
        to disable the automatic interpeting of the dependency name as a json pointer path,
        regardless of any containing slashes.

        If accessing pandas, you may pass an already splitted path with
        its last *part* being a callable indexer (:ref:`pandas:indexing.callable`).

        In addition to writing values, the :func:`.vcat` or :func:`.hcat` modifiers
        (& respective accessors) support also `pandas concatenation` for `provides`
        (see example in :ref:`jsnop-df-concat`).
    :param implicit:
        :term:`implicit` dependencies are not fed into/out of the function.
        You may use directly :func:`implicit`.
    :param accessor:
        Annotate the `dependency` with :term:`accessor` functions to read/write
        `solution` (actually a 2-tuple with functions is ok)

    **Example:**

    Let's use *json pointer dependencies* along with the default :term:`conveyor operation`
    to build an operation copying values around in the solution:

        >>> from graphtik import operation, compose, modify

        >>> copy_values = operation(
        ...     fn=None,  # ask for the "conveyor op"
        ...     name="copy a+b-->A+BB",
        ...     needs=["inputs/a", "inputs/b"],
        ...     provides=["RESULTS/A", "RESULTS/BB"]
        ... )

        >>> results = copy_values.compute({"inputs": {"a": 1, "b": 2}})
        Traceback (most recent call last):
        ValueError: Failed matching inputs <=> needs for FnOp(name='copy a+b-->A+BB',
            needs=['inputs/a'($), 'inputs/b'($)],
            provides=['RESULTS/A'($), 'RESULTS/BB'($)],
            fn='identity_fn'):
            1. Missing compulsory needs['inputs/a'($), 'inputs/b'($)]!
            +++inputs: ['inputs']

        >>> results = copy_values.compute({"inputs/a": 1, "inputs/b": 2})
        >>> results
        {'RESULTS/A'($): 1, 'RESULTS/BB'($): 2}

    Notice that the :term:`hierarchical dependencies <subdoc>` did not yet worked,
    because *jsonp* modifiers work internally with :term:`accessor`\\s, and
    :class:`.FnOp` is unaware of them -- it's the :class:`.Solution`
    class that supports *accessors**, and this requires the operation to be wrapped
    in a pipeline (see below).

    Note also that it we see the "representation' of the key as ``'RESULTS/A'($)``
    but the actual string value simpler:

        >>> str(next(iter(results)))
        'RESULTS/A'

    The results were not nested, because this modifer works with :term:`accessor` functions,
    that act only on a real :class:`.Solution`, given to the operation only when wrapped
    in a pipeline (as done below).

    Now watch how these paths access deep into solution when the same operation
    is wrapped in a pipeline:

        >>> pipe = compose("copy pipe", copy_values)
        >>> sol = pipe.compute({"inputs": {"a": 1, "b": 2}}, outputs="RESULTS")
        >>> sol
        {'RESULTS': {'A': 1, 'BB': 2}}

    .. graphtik::
    """
    return _modifier(
        name, keyword=keyword, jsonp=jsonp, implicit=implicit, accessor=accessor
    )


def implicit(name, *, jsonp=None) -> _Modifier:
    """see :term:`implicit` & generic :func:`.modify` modifier. """
    return _modifier(name, implicit=True, jsonp=jsonp)


def vcat(name, *, keyword: str = None, jsonp=None) -> _Modifier:
    """Provides-only, see :term:`pandas concatenation` & generic :func:`.modify` modifier. """
    return _modifier(name, accessor=VCatAcc(), keyword=keyword, jsonp=jsonp)


def hcat(name, *, keyword: str = None, jsonp=None) -> _Modifier:
    """Provides-only, see :term:`pandas concatenation` & generic :func:`.modify` modifier. """
    return _modifier(name, accessor=HCatAcc(), keyword=keyword, jsonp=jsonp)


def keyword(
    name: str, keyword: str = None, accessor: Accessor = None, jsonp=None
) -> _Modifier:
    """
    Annotate a :term:`dependency` that maps to a different name in the underlying function.

    When used on :term:`needs` dependencies:

    * The value of the ``name`` dependency is read from the `solution`, and then
    * that value is passed in the function as a *keyword-argument* named ``keyword``.

    When used on :term:`provides` dependencies:

    * The operation must be a :term:`returns dictionary`.
    * The value keyed with ``keyword`` is read from function's returned dictionary,
      and then
    * that value is placed into `solution` named as ``name``.

    :param keyword:
        The argument-name corresponding to this named-input.
        If it is None, assumed the same as `name`, so as
        to behave always like kw-type arg, and to preserve its fn-name
        if ever renamed.

        .. Note::
            This extra mapping argument is needed either for :term:`optionals`
            (but not :term:`varargish`), or for functions with keywords-only arguments
            (like ``def func(*, foo, bar): ...``),
            since `inputs` are normally fed into functions by-position, not by-name.
    :param accessor:
        the functions to access values to/from solution (see :class:`Accessor`)
        (actually a 2-tuple with functions is ok)
    :param jsonp:
        None (derrived from `name`), ``False``, str, collection of str/callable (last one)
        See generic :func:`.modify` modifier.

    :return:
        a :class:`_Modifier` instance, even if no `keyword` is given OR
        it is the same as `name`.

    **Example:**

    In case the name of a function input argument is different from the name in the
    :term:`graph` (or just because the name in the `inputs` is not a valid argument-name),
    you may *map* it with the 2nd argument of :func:`.keyword`:

        >>> from graphtik import operation, compose, keyword

        >>> @operation(needs=[keyword("name-in-inputs", "fn_name")], provides="result")
        ... def foo(*, fn_name):  # it works also with non-positional args
        ...    return fn_name
        >>> foo
        FnOp(name='foo',
             needs=['name-in-inputs'(>'fn_name')],
             provides=['result'],
             fn='foo')

        >>> pipe = compose('map a need', foo)
        >>> pipe
        Pipeline('map a need', needs=['name-in-inputs'], provides=['result'], x1 ops: foo)

        >>> sol = pipe.compute({"name-in-inputs": 4})
        >>> sol['result']
        4

        .. graphtik::

    You can do the same thing to the results of a :term:`returns dictionary` operation:

        >>> op = operation(lambda: {"fn key": 1},
        ...                name="renaming `provides` with a `keyword`",
        ...                provides=keyword("graph key", "fn key"),
        ...                returns_dict=True)
        >>> op
        FnOp(name='renaming `provides` with a `keyword`',
             provides=['graph key'(>'fn key')],
             fn{}='<lambda>')

    .. graphtik::

    .. hint::
        Mapping `provides` names wouldn't make sense for regular operations, since
        these are defined arbitrarily at the operation level.
        OTOH, the result names of :term:`returns dictionary` operation are decided
        by the underlying function, which may lie beyond the control of the user
        (e.g. from a 3rd-party object).
    """
    # Must pass a truthy `keyword` bc cstor cannot not know its keyword.
    return _modifier(name, keyword=keyword or name, accessor=accessor, jsonp=jsonp)


def optional(
    name: str, keyword: str = None, accessor: Accessor = None, jsonp=None, implicit=None
) -> _Modifier:
    """
    Annotate :term:`optionals` `needs` corresponding to *defaulted* op-function arguments, ...

    received only if present in the `inputs` (when operation is invoked).

    The value of an *optional* dependency is passed in as a *keyword argument*
    to the underlying function.

    :param keyword:
        the name for the function argument it corresponds;
        if a falsy is given, same as `name` assumed,
        to behave always like kw-type arg and to preserve its fn-name
        if ever renamed.
    :param accessor:
        the functions to access values to/from solution (see :class:`Accessor`)
        (actually a 2-tuple with functions is ok)
    :param jsonp:
        None (derrived from `name`), ``False``, str, collection of str/callable (last one)
        See generic :func:`.modify` modifier.
    :param implicit:
        :term:`implicit` dependencies are not fed into/out of the function.
        You may use directly :func:`implicit`.

    **Example:**

        >>> from graphtik import operation, compose, optional

        >>> @operation(name='myadd',
        ...            needs=["a", optional("b")],
        ...            provides="sum")
        ... def myadd(a, b=0):
        ...    return a + b

    Notice the default value ``0`` to the ``b`` annotated as optional argument:

        >>> graph = compose('mygraph', myadd)
        >>> graph
        Pipeline('mygraph',
                         needs=['a', 'b'(?)],
                         provides=['sum'],
                         x1 ops: myadd)

    .. graphtik::

    The graph works both with and without ``c`` provided in the inputs:

        >>> graph(a=5, b=4)['sum']
        9
        >>> graph(a=5)
        {'a': 5, 'sum': 5}

    Like :func:`.keyword` you may map input-name to a different function-argument:

        >>> operation(needs=['a', optional("quasi-real", "b")],
        ...           provides="sum"
        ... )(myadd.fn)  # Cannot wrap an operation, its `fn` only.
        FnOp(name='myadd',
                            needs=['a', 'quasi-real'(?'b')],
                            provides=['sum'],
                            fn='myadd')

    """
    # Must pass a truthy `keyword` as cstor-matrix requires.
    return _modifier(
        name,
        keyword=keyword or name,
        optional=_Optionals.keyword,
        accessor=accessor,
        jsonp=jsonp,
        implicit=implicit,
    )


def vararg(name: str, accessor: Accessor = None, jsonp=None) -> _Modifier:
    """
    Annotate a :term:`varargish` `needs` to  be fed as function's ``*args``.

    :param accessor:
        the functions to access values to/from solution (see :class:`Accessor`)
        (actually a 2-tuple with functions is ok)
    :param jsonp:
        None (derrived from `name`), ``False``, str, collection of str/callable (last one)
        See generic :func:`.modify` modifier.

    .. seealso::
        Consult also the example test-case in: :file:`test/test_op.py:test_varargs()`,
        in the full sources of the project.

    **Example:**

    We designate ``b`` & ``c`` as `vararg` arguments:

        >>> from graphtik import operation, compose, vararg

        >>> @operation(
        ...     needs=['a', vararg('b'), vararg('c')],
        ...     provides='sum'
        ... )
        ... def addall(a, *b):
        ...    return a + sum(b)
        >>> addall
        FnOp(name='addall',
                            needs=['a', 'b'(*), 'c'(*)],
                            provides=['sum'],
                            fn='addall')


        >>> graph = compose('mygraph', addall)

    .. graphtik::

    The graph works with and without any of ``b`` or ``c`` inputs:

        >>> graph(a=5, b=2, c=4)['sum']
        11
        >>> graph(a=5, b=2)
        {'a': 5, 'b': 2, 'sum': 7}
        >>> graph(a=5)
        {'a': 5, 'sum': 5}

    """
    return _modifier(name, optional=_Optionals.vararg, accessor=accessor, jsonp=jsonp)


def varargs(name: str, accessor: Accessor = None, jsonp=None) -> _Modifier:
    """
    An :term:`varargish`  :func:`.vararg`, naming a *iterable* value in the inputs.

    :param accessor:
        the functions to access values to/from solution (see :class:`Accessor`)
        (actually a 2-tuple with functions is ok)
    :param jsonp:
        None (derrived from `name`), ``False``, str, collection of str/callable (last one)
        See generic :func:`.modify` modifier.

    .. seealso::
        Consult also the example test-case in: :file:`test/test_op.py:test_varargs()`,
        in the full sources of the project.

    **Example:**

        >>> from graphtik import operation, compose, varargs

        >>> def enlist(a, *b):
        ...    return [a] + list(b)

        >>> graph = compose('mygraph',
        ...     operation(name='enlist', needs=['a', varargs('b')],
        ...     provides='sum')(enlist)
        ... )
        >>> graph
        Pipeline('mygraph',
                         needs=['a', 'b'(?)],
                         provides=['sum'],
                         x1 ops: enlist)

    .. graphtik::

    The graph works with or without `b` in the inputs:

        >>> graph(a=5, b=[2, 20])['sum']
        [5, 2, 20]
        >>> graph(a=5)
        {'a': 5, 'sum': [5]}
        >>> graph(a=5, b=0xBAD)
        Traceback (most recent call last):
        ValueError: Failed matching inputs <=> needs for FnOp(name='enlist',
                needs=['a', 'b'(+)], provides=['sum'], fn='enlist'):
            1. Expected varargs inputs to be non-str iterables: {'b'(+): 2989}
            +++inputs: ['a', 'b']

    .. varargs-mistake-start
    .. Attention::
        To avoid user mistakes, *varargs* do not accept :class:`str` :term:`inputs`
        (though iterables):

        >>> graph(a=5, b="mistake")
        Traceback (most recent call last):
        ValueError: Failed matching inputs <=> needs for FnOp(name='enlist',
                    needs=['a', 'b'(+)],
                    provides=['sum'],
                    fn='enlist'):
            1. Expected varargs inputs to be non-str iterables: {'b'(+): 'mistake'}
            +++inputs: ['a', 'b']

    .. varargs-mistake-end

    .. seealso::
        The elaborate example in :ref:`hierarchical-data` section.
    """
    return _modifier(name, optional=_Optionals.varargs, accessor=accessor, jsonp=jsonp)


def sfx(name, optional: bool = None) -> _Modifier:
    """
    :term:`sideffects` denoting modifications beyond the scope of the solution.

    Both `needs` & `provides` may be designated as *sideffects* using this modifier.
    They work as usual while solving the graph (:term:`planning`) but
    they have a limited interaction with the operation's underlying function;
    specifically:

    - input sideffects must exist in the solution as :term:`inputs` for an operation
      depending on it to kick-in, when the computation starts - but this is not necessary
      for intermediate sideffects in the solution during execution;
    - input sideffects are NOT fed into underlying functions;
    - output sideffects are not expected from underlying functions, unless
      a rescheduled operation with :term:`partial outputs` designates a sideffected
      as *canceled* by returning it with a falsy value (operation must `returns dictionary`).

    .. hint::
        If modifications involve some input/output, prefer the :func:`.sfxed`
        modifier.

        You may still convey this relationships by including the dependency name
        in the string - in the end, it's just a string - but no enforcement of any kind
        will happen from *graphtik*, like:

        >>> from graphtik import sfx

        >>> sfx("price[sales_df]")
        sfx('price[sales_df]')

    **Example:**

    A typical use-case is to signify changes in some "global" context,
    outside `solution`:


        >>> from graphtik import operation, compose, sfx

        >>> @operation(provides=sfx("lights off"))  # sideffect names can be anything
        ... def close_the_lights():
        ...    pass

        >>> graph = compose('strip ease',
        ...     close_the_lights,
        ...     operation(
        ...         name='undress',
        ...         needs=[sfx("lights off")],
        ...         provides="body")(lambda: "TaDa!")
        ... )
        >>> graph
        Pipeline('strip ease',
                         needs=[sfx('lights off')],
                         provides=[sfx('lights off'), 'body'],
                         x2 ops: close_the_lights, undress)

        >>> sol = graph()
        >>> sol
        {'body': 'TaDa!'}

    .. graphtik::
        :name: sideffect

    .. note::
        Something has to provide a sideffect for a function needing it to execute -
        this could be another operation, like above, or the user-inputs;
        just specify some truthy value for the sideffect:

            >>> sol = graph.compute({sfx("lights off"): True})

        .. graphtik::

    """
    return _modifier(
        name, optional=_Optionals.keyword if optional else None, sideffected=name
    )


def sfxed(
    dependency: str,
    sfx0: str,
    *sfx_list: str,
    keyword: str = None,
    optional: bool = None,
    accessor: Accessor = None,
    jsonp=None,
) -> _Modifier:
    r"""
    Annotates a :term:`sideffected` dependency in the solution sustaining side-effects.

    :param dependency:
        the actual dependency receiving the sideffect, which will be fed into/out
        of the function.
    :param sfx0:
        the 1st (arbitrary object) sideffect marked as "acting" on the `dependency`.
    :param sfx0:
        more (arbitrary object) sideffects (like the `sfx0`)
    :param keyword:
        the name for the function argument it corresponds.
        When optional, it becomes the same as `name` if falsy, so as
        to behave always like kw-type arg, and to preserve fn-name if ever renamed.
        When not optional, if not given, it's all fine.
    :param accessor:
        the functions to access values to/from solution (see :class:`Accessor`)
        (actually a 2-tuple with functions is ok)
    :param jsonp:
        None (derrived from `name`), ``False``, str, collection of str/callable (last one)
        See generic :func:`.modify` modifier.

    Like :func:`.sfx` but annotating a *real* :term:`dependency` in the solution,
    allowing that dependency to be present both in :term:`needs` and :term:`provides`
    of the same function.

    **Example:**

    A typical use-case is to signify columns required to produce new ones in
    pandas dataframes (:gray:`emulated with dictionaries`):


        >>> from graphtik import operation, compose, sfxed

        >>> @operation(needs="order_items",
        ...            provides=sfxed("ORDER", "Items", "Prices"))
        ... def new_order(items: list) -> "pd.DataFrame":
        ...     order = {"items": items}
        ...     # Pretend we get the prices from sales.
        ...     order['prices'] = list(range(1, len(order['items']) + 1))
        ...     return order

        >>> @operation(
        ...     needs=[sfxed("ORDER", "Items"), "vat rate"],
        ...     provides=sfxed("ORDER", "VAT")
        ... )
        ... def fill_in_vat(order: "pd.DataFrame", vat: float):
        ...     order['VAT'] = [i * vat for i in order['prices']]
        ...     return order

        >>> @operation(
        ...     needs=[sfxed("ORDER", "Prices", "VAT")],
        ...     provides=sfxed("ORDER", "Totals")
        ... )
        ... def finalize_prices(order: "pd.DataFrame"):
        ...     order['totals'] = [p + v for p, v in zip(order['prices'], order['VAT'])]
        ...     return order

    To view all internal :term:`dependencies <dependency>`, enable DEBUG
    in :term:`configurations`:

        >>> from graphtik.config import debug_enabled

        >>> with debug_enabled(True):
        ...     finalize_prices
        FnOp(name='finalize_prices',
             needs=[sfxed('ORDER', 'Prices'), sfxed('ORDER', 'VAT')],
             _user_needs=[sfxed('ORDER', 'Prices', 'VAT')],
             _fn_needs=['ORDER'], provides=[sfxed('ORDER', 'Totals')],
             _user_provides=[sfxed('ORDER', 'Totals')],
             _fn_provides=['ORDER'],
             fn='finalize_prices')

    Notice that declaring a single *sideffected* with many items in `sfx_list`,
    expands into multiple  *"singular"* ``sideffected`` dependencies in the network
    (check ``needs`` vs ``_user_needs`` above).

        >>> proc_order = compose('process order', new_order, fill_in_vat, finalize_prices)
        >>> sol = proc_order.compute({
        ...      "order_items": ["toilet-paper", "soap"],
        ...      "vat rate": 0.18,
        ... })
        >>> sol
        {'order_items': ['toilet-paper', 'soap'],
         'vat rate': 0.18,
         'ORDER': {'items': ['toilet-paper', 'soap'],
                   'prices': [1, 2],
                   'VAT': [0.18, 0.36],
                   'totals': [1.18, 2.36]}}

    .. graphtik::
        :height: 640
        :width: 100%
        :name: sideffecteds

    Notice that although many functions consume & produce the same ``ORDER`` dependency,
    something that :orange:`would have formed cycles`, the wrapping operations
    *need* and *provide* different *sideffected* instances,
    :green:`breaking thus the cycles`.

    .. seealso::
        The elaborate example in :ref:`hierarchical-data` section.
    """
    return _modifier(
        dependency,
        optional=_Optionals.keyword if optional else None,
        keyword=dependency if optional and not keyword else keyword,
        sideffected=dependency,
        sfx_list=(sfx0, *sfx_list),
        accessor=accessor,
        jsonp=jsonp,
    )


def sfxed_vararg(
    dependency: str, sfx0: str, *sfx_list: str, accessor: Accessor = None, jsonp=None
) -> _Modifier:
    """Like :func:`sideffected` + :func:`vararg`. """
    return _modifier(
        dependency,
        optional=_Optionals.vararg,
        sideffected=dependency,
        sfx_list=(sfx0, *sfx_list),
        accessor=accessor,
        jsonp=jsonp,
    )


def sfxed_varargs(
    dependency: str, sfx0: str, *sfx_list: str, accessor: Accessor = None, jsonp=None
) -> _Modifier:
    """Like :func:`sideffected` + :func:`varargs`. """
    return _modifier(
        dependency,
        optional=_Optionals.varargs,
        sideffected=dependency,
        sfx_list=(sfx0, *sfx_list),
        accessor=accessor,
        jsonp=jsonp,
    )
