=========
circuitdb
=========

Data set of optimal circuits for Boolean functions that have low arity.

|pypi| |travis| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/circuitdb.svg
   :target: https://badge.fury.io/py/circuitdb
   :alt: PyPI version and link.

.. |travis| image:: https://travis-ci.com/reity/circuitdb.svg?branch=master
   :target: https://travis-ci.com/reity/circuitdb

.. |coveralls| image:: https://coveralls.io/repos/github/reity/circuitdb/badge.svg?branch=master
   :target: https://coveralls.io/github/reity/circuitdb?branch=master

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install circuitdb

The library can be imported in the usual ways::

    import circuitdb
    from circuitdb import circuitdb

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `nose <https://nose.readthedocs.io/>`_ (see ``setup.cfg`` for configution details)::

    nosetests

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python circuitdb/circuitdb.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    pylint circuitdb

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the GitHub page for this library.

Versioning
----------
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.
