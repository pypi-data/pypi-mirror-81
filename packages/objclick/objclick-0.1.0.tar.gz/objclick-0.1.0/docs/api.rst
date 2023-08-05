API Documentation
=================

The `objclick` module provides a drop-in replacement for `click`.  The
top-level namespace of `click` is imported into the top-level namespace of
`objclick`, so it can be used like::

    >>> import objclick as click

However, this drop-in does pertain to any sub-modules of `click`.  Only
those functions that differ from the default behavior of `click` are
documented here.


.. automodule:: objclick


Decorators
----------

All decorators defined by `objclick` are importable from the top-level
package namespace (e.g. `objclick.command`).

.. autofunction:: objclick.command

.. autofunction:: objclick.group

.. autofunction:: objclick.classcommand

.. autofunction:: objclick.classgroup

.. autofunction:: objclick.with_context


Internals
---------

.. automodule:: objclick.objclick
    :members:
