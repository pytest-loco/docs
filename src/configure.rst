Configure
=========

.. warning::
   Current version has not been tested in parallel execution mode.
   This task is in the backlog and is required for the stable release. We recommend
   avoiding plugins like ``pytest-xdist`` with ``pytest-loco``; it is best to run
   pytest with the ``-n 0`` flag until the stable version is released.

Command-line options
--------------------

``pytest-loco`` registers the following command-line flags
that can be passed to pytest directly.

``--loco-unsafe-yaml``
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console
   :caption: Enable unsafe YAML loading with pytest-loco

   pytest --loco-unsafe-yaml

Allows loading YAML files using the unsafe PyYAML ``Loader``
instead of the default ``SafeLoader``. This enables execution
of arbitrary Python objects embedded in YAML documents.

``--loco-relaxed``
^^^^^^^^^^^^^^^^^^

.. code-block:: console
   :caption: Enable relaxed mode for pytest-loco

   pytest --loco-relaxed

Disables strict DSL validation. In relaxed mode:

- Field rewriting and shadowing in step or case documents does not cause a failure.
- Errors from loading third-party plugins do not abort collection or execution.

Use this flag when integrating pytest-loco into an existing
project where strict schema enforcement is not yet required.

``--loco-allow-lambda``
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   pytest --loco-allow-lambda

Allows inline lambda expressions inside DSL documents.

Persistent configuration
-------------------------

To avoid passing flags on every run, add them to your ``pyproject.toml`` under
the ``[tool.pytest.ini_options]`` section (or to a ``pytest.ini`` file) to set
them as defaults for pytest:

.. tab:: pyproject.toml

   .. code-block:: toml
      :caption: Relaxed mode for pytest-loco in pyproject.toml

      [tool.pytest.ini_options]
      addopts = "--loco-relaxed"

.. tab:: pytest.ini

   .. code-block:: ini
      :caption: Relaxed mode for pytest-loco in pytest.ini

      [pytest]
      addopts = --loco-relaxed
