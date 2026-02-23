JSON
====

pytest-loco-json
----------------

The ``pytest-loco-json`` extension adds first-class JSON support to the ``pytest-loco`` DSL.
It provides facilities for decoding, encoding, and querying JSON data as part of test execution
Once enabled, JSON becomes a native data format within the DSL, suitable for validation, transformation,
and data-driven testing scenarios with ``!dump`` and ``!load`` instructions.

Installation
------------

Requires Python 3.13 or newer.

.. tab:: User

   .. code-block:: console
      :caption: Install from PyPI 

      pip install pytest-loco-json

.. tab:: Poetry Project

   .. code-block:: console
      :caption: Install from PyPI 

      poetry add pytest-loco-json


After installation extension provides:

.. toctree::
   :maxdepth: 1

   formats
   instructions
