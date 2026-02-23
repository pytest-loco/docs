pytest-loco
============

.. toctree::
   :hidden:

   get-started
   configure

.. toctree::
   :caption: Concepts
   :hidden:

   concepts/case
   concepts/step
   concepts/instruction
   concepts/format
   concepts/context
   concepts/template

.. toctree::
   :caption: Core Extensions
   :hidden:

   extensions/http/index
   extensions/json/index

.. toctree::
   :caption: Integrations
   :hidden:

   integrations/vscode

Declarative DSL for structured, extensible test scenarios in pytest.

``pytest-loco`` introduces a YAML-based domain-specific language (DSL) for describing
test workflows in a declarative and composable way. It is designed to support structured
validation, data-driven execution, and pluggable extensions such as HTTP, JSON,
and custom domain logic.

Installation
------------

Requires Python 3.13 or newer.

.. tab:: User

   .. code-block:: console
      :caption: Install from PyPI 

      pip install pytest-loco

.. tab:: Poetry Project

   .. code-block:: console
      :caption: Install from PyPI 

      poetry add pytest-loco

After installation, verify that the plugin is discovered by pytest:

.. tab:: User

   .. code-block:: console
      :caption: Verify installation

      pytest --trace-config

.. tab:: Poetry Project

   .. code-block:: console
      :caption: Verify installation

      poetry run pytest --trace-config

You should see ``pytest-loco`` listed in registered third-party plugins block.

Bugs/Requests
-------------

Please use the `GitHub issue tracker <https://github.com/pytest-loco/pytest-loco/issues>`_
to submit bugs or request features.
