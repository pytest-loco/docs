HTTP
====

pytest-loco-http
----------------

The ``pytest-loco-http`` extension provides first-class HTTP support for the ``pytest-loco`` DSL.
It introduces a set of HTTP actors (``http.get``, ``http.post``, ``http.put``, ``http.delete``, etc.)
that execute HTTP requests using managed sessions and return normalized, structured response objects.

Installation
------------

Requires Python 3.13 or newer.

.. tab:: User

   .. code-block:: console
      :caption: Install from PyPI 

      pip install pytest-loco-http

.. tab:: Poetry Project

   .. code-block:: console
      :caption: Install from PyPI 

      poetry add pytest-loco-http


After installation extension provides:

.. toctree::
   :maxdepth: 1

   actions
   instructions
