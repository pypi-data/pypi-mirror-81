Python ``raise`` as a Function
==============================

Raise exceptions with a function instead of a statement.

Provides a minimal, clean, and portable interface for raising
exceptions with all the advantages of functions over syntax.


Versioning
----------

This library's version numbers follow the `SemVer 2.0.0 specification
<https://semver.org/spec/v2.0.0.html>`_.


Installation
------------

::

    pip install raise

If you need to get it manually, or you need the "no traceback"
variant, see the `Manual Installation`_ section for tips.


Usage
-----

Import ``raise_``:

.. code:: python

    from raise_ import raise_

Raise an exception:

.. code:: python

    raise_(Exception('foo'))

Raise an exception with a traceback:

.. code:: python

    raise_(Exception('foo'), traceback)

Raise in a ``lambda``:

.. code:: python

    lambda x: x if x > 0 else raise_(ValueError('x is too small!')) 

And of course because ``raise_`` is a function,
you can combine it with ``functools.partial``
and other functional programming libraries and
techniques for many more uses.


Surprises
---------

In Python 3, the ``raise`` **statement** reuses the
``__traceback__`` attribute every time it raises an
exception unless you explicitly set another traceback.
The ``raise_`` **function** does *not* reuse
``__traceback__``, and instead clears it if you do
not pass in a traceback, as if you passed in ``None``.
If you want the Python 3 behavior of reusing the
``__traceback__``, you should explicitly pass it in:

.. code:: python

    raise_(exception, exception.__traceback__)

Or, if you want to gracefully degrade on
Python implementations which do not have
``__traceback__`` on their exceptions:

.. code:: python

    raise_(exception, getattr(exception, '__traceback__', None))


Portability
-----------

Portable to all releases of both Python 3 and Python 2.

(The oldest tested is 2.5, but it will likely work on all
Python 2 versions and probably on even earlier versions.)

For implementations of Python that do not support raising
with a custom traceback, a "no traceback" variant can be
installed manually.


Manual Installation
-------------------

Depending on your needs, either:

* Take one of these files and save it as ``raise_.py``:

  * ``raise_3.py`` is for Python 3.
  * ``raise_2.py`` is for Python 2.
  * ``raise_no_traceback.py`` is for Python implementations which
    do not support raising exceptions with a custom traceback.

* Take all of the above files and the ``__init__.py``
  file and save them in a folder called ``raise_``.

That way you can always do ``from raise_ import raise_``
in all of your other code and it'll just work.

You are of course welcome to just copy-paste the tiny ``raise_``
function definition into your code, just keep in mind the
compatibility issues involved: your code will only work without
modification on Python versions compatible with the version you
chose, and Python 2's version causes a SyntaxError in Python 3.
