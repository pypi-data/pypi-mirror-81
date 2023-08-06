# Copyright 2016, Yahoo Inc.
# Licensed under the terms of the Apache License, Version 2.0. See the LICENSE file associated with the project for terms.
"""
:term:`configurations` for network execution, and utilities on them.

.. seealso:: methods :func:`.plot.active_plotter_plugged()`, :func:`.plot.set_active_plotter()`,
    :func:`.plot.get_active_plotter()`

    Plot configrations were not defined here, not to pollute import space early,
    until they are actually needed.

.. note::
    The contant-manager function ``XXX_plugged()`` or ``XXX_enabled()`` do NOT launch
    their code blocks using :meth:`contextvars.Context.run()` in a separate "context",
    so any changes to these or other context-vars will persist
    (unless they are also done within such context-managers)
"""
import ctypes
import os
from contextlib import contextmanager
from contextvars import ContextVar
from functools import partial
from multiprocessing import Value
from typing import Optional

_debug_env_var = os.environ.get("GRAPHTIK_DEBUG")
_debug: ContextVar[Optional[bool]] = ContextVar(
    "debug",
    default=_debug_env_var and (_debug_env_var.lower() not in "0 false off no".split()),
)
_abort: ContextVar[Optional[bool]] = ContextVar(
    "abort", default=Value(ctypes.c_bool, lock=False)
)
_skip_evictions: ContextVar[Optional[bool]] = ContextVar("skip_evictions", default=None)
_layered_solution: ContextVar[Optional[bool]] = ContextVar(
    "layered_solution", default=None
)
_execution_pool: ContextVar[Optional["Pool"]] = ContextVar(
    "execution_pool", default=None
)
_parallel_tasks: ContextVar[Optional[bool]] = ContextVar("parallel_tasks", default=None)
_marshal_tasks: ContextVar[Optional[bool]] = ContextVar("marshal_tasks", default=None)
_endure_operations: ContextVar[Optional[bool]] = ContextVar(
    "endure_operations", default=None
)
_reschedule_operations: ContextVar[Optional[bool]] = ContextVar(
    "reschedule_operations", default=None
)


def _getter(context_var) -> Optional[bool]:
    return context_var.get()


@contextmanager
def _tristate_set(context_var, enabled):
    return context_var.set(enabled if enabled is None else bool(enabled))


@contextmanager
def _tristate_armed(context_var: ContextVar, enabled=True):
    """Assumes "enabled" if `enabled` flag is None."""
    resetter = context_var.set(enabled if enabled is None else bool(enabled))
    try:
        yield
    finally:
        context_var.reset(resetter)


debug_enabled = partial(_tristate_armed, _debug)
"""
Like :func:`set_debug()` as a context-manager, resetting back to old value.

.. seealso:: disclaimer about context-managers at the top of this :mod:`.config` module.
"""
is_debug = partial(_getter, _debug)
"""
Return :func:`.set_debug` or `True` if :envvar:`GRAPHTIK_DEBUG` not one of ``0 false off no``.

Affected behavior when :ref:`debug` enabled:

.. debug-behavior-start

+ on errors, plots the 1st errored solution/plan/pipeline/net (in that order)
  in an SVG file inside the temp-directory, and its path is logged in ERROR-level;
+ :term:`jetsam` logs in ERROR (instead of in DEBUG) all annotations on all calls
  up the stack trace (logged from ``graphtik.jetsam.err`` logger);
+ :meth:`FnOp.compute()` prints out full given-inputs (not just their keys);
+ net objects print more details recursively, like fields (not just op-names) and
  prune-comments;
+ plotted SVG diagrams include style-provenance as tooltips;
+ Sphinx extension also saves the original DOT file next to each image
  (see :confval:`graphtik_save_dot_files`).

.. debug-behavior-end

.. Note::
    The default is controlled with :envvar:`GRAPHTIK_DEBUG` environment variable.

Note that enabling this flag is different from enabling logging in DEBUG,
since it affects all code (eg interactive printing in debugger session,
exceptions, doctests), not just debug statements (also affected by this flag).

:return:
    a "reset" token (see :meth:`.ContextVar.set`)
"""
set_debug = partial(_tristate_set, _debug)
"""
Enable/disable debug-mode.

:param enabled:
    - ``None, False, string(0, false, off, no)``: Disabled
    - anything else: Enable DEBUG

see :func:`is_debug()`
"""


def abort_run():
    """
    Sets the :term:`abort run` global flag, to halt all currently or future executing plans.

    This global flag is reset when any :meth:`.Pipeline.compute()` is executed,
    or manually, by calling :func:`.reset_abort()`.
    """
    _abort.get().value = True


def reset_abort():
    """Reset the :term:`abort run` global flag, to permit plan executions to proceed. """
    _abort.get().value = False


def is_abort():
    """Return `True` if networks have been signaled to stop :term:`execution`."""
    return _abort.get().value


evictions_skipped = partial(_tristate_armed, _skip_evictions)
"""
Like :func:`set_skip_evictions()` as a context-manager, resetting back to old value.

.. seealso:: disclaimer about context-managers at the top of this :mod:`.config` module.
"""
is_skip_evictions = partial(_getter, _skip_evictions)
"""see :func:`set_skip_evictions()`"""
set_skip_evictions = partial(_tristate_set, _skip_evictions)
"""
When true, disable globally :term:`eviction`\\s, to keep all intermediate solution values, ...

regardless of asked outputs.

:return:
    a "reset" token (see :meth:`.ContextVar.set`)
"""


solution_layered = partial(_tristate_armed, _layered_solution)
"""
Like :func:`set_layered_solution()` as a context-manager, resetting back to old value.

.. seealso:: disclaimer about context-managers at the top of this :mod:`.config` module.
"""
is_layered_solution = partial(_getter, _layered_solution)
"""see :func:`set_layered_solution()`"""
set_layered_solution = partial(_tristate_set, _layered_solution)
"""
whether to store operation results into separate :term:`solution layer`

:param enable:
    If false/true, it overrides any param given when executing a pipeline or a plan.
    If None (default), results are layered only if there are NO :term:`jsonp` dependencies
    in the network.

:return:
    a "reset" token (see :meth:`.ContextVar.set`)
"""


@contextmanager
def execution_pool_plugged(pool: "Optional[Pool]"):
    """
    Like :func:`set_execution_pool()` as a context-manager, resetting back to old value.

    .. seealso:: disclaimer about context-managers at the top of this :mod:`.config` module.
    """
    resetter = _execution_pool.set(pool)
    try:
        yield
    finally:
        _execution_pool.reset(resetter)


def set_execution_pool(pool: "Optional[Pool]"):
    """
    (deprecated) Set the process-pool for :term:`parallel` plan executions.

    You may have to :also func:`set_marshal_tasks()` to resolve
    pickling issues.
    """
    return _execution_pool.set(pool)


def get_execution_pool() -> "Optional[Pool]":
    """(deprecated) Get the process-pool for :term:`parallel` plan executions."""
    return _execution_pool.get()


tasks_in_parallel = partial(_tristate_armed, _parallel_tasks)
"""
(deprecated) Like :func:`set_parallel_tasks()` as a context-manager, resetting back to old value.

.. seealso:: disclaimer about context-managers at the top of this :mod:`.config` module.
"""
is_parallel_tasks = partial(_getter, _parallel_tasks)
"""see :func:`set_parallel_tasks()`"""
set_parallel_tasks = partial(_tristate_set, _parallel_tasks)
"""
Enable/disable globally :term:`parallel` execution of operations.

:param enable:
    - If ``None`` (default), respect the respective flag on each operation;
    - If true/false, force it for all operations.

:return:
    a "reset" token (see :meth:`.ContextVar.set`)
"""


tasks_marshalled = partial(_tristate_armed, _marshal_tasks)
"""
(deprecated) Like :func:`set_marshal_tasks()` as a context-manager, resetting back to old value.

.. seealso:: disclaimer about context-managers at the top of this :mod:`.config` module.
"""
is_marshal_tasks = partial(_getter, _marshal_tasks)
"""(deprecated) see :func:`set_marshal_tasks()`"""
set_marshal_tasks = partial(_tristate_set, _marshal_tasks)
"""
(deprecated) Enable/disable globally :term:`marshalling` of :term:`parallel` operations, ...

inputs & outputs with :mod:`dill`,  which might help for pickling problems.

:param enable:
    - If ``None`` (default), respect the respective flag on each operation;
    - If true/false, force it for all operations.

:return:
    a "reset" token (see :meth:`.ContextVar.set`)
"""


operations_endured = partial(_tristate_armed, _endure_operations)
"""
Like :func:`set_endure_operations()` as a context-manager, resetting back to old value.

.. seealso:: disclaimer about context-managers at the top of this :mod:`.config` module.
"""
is_endure_operations = partial(_getter, _endure_operations)
"""see :func:`set_endure_operations()`"""
set_endure_operations = partial(_tristate_set, _endure_operations)
"""
Enable/disable globally :term:`endurance` to keep executing even if some operations fail.

:param enable:
    - If ``None`` (default), respect the flag on each operation;
    - If true/false, force it for all operations.

:return:
    a "reset" token (see :meth:`.ContextVar.set`)

."""


operations_reschedullled = partial(_tristate_armed, _reschedule_operations)
"""
Like :func:`set_reschedule_operations()` as a context-manager, resetting back to old value.

.. seealso:: disclaimer about context-managers at the top of this :mod:`.config` module.
"""
is_reschedule_operations = partial(_getter, _reschedule_operations)
"""see :func:`set_reschedule_operations()`"""
set_reschedule_operations = partial(_tristate_set, _reschedule_operations)
"""
Enable/disable globally :term:`rescheduling` for operations returning only *partial outputs*.

:param enable:
    - If ``None`` (default), respect the flag on each operation;
    - If true/false, force it for all operations.

:return:
    a "reset" token (see :meth:`.ContextVar.set`)

."""
