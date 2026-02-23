Get Started
===========

Create a project
----------------

**Prerequisites**: Python 3.13 and
`Poetry <https://python-poetry.org/docs/#installation>`_
must be installed.

Create a new Poetry project and add pytest-loco as a dependency:

.. code-block:: console
   :caption: Create a new Poetry project and add pytest-loco

   poetry new example-project
   cd example-project
   poetry add pytest-loco

To test HTTP services, also add the HTTP extension:

.. code-block:: console
   :caption: Add the HTTP extension for testing HTTP services

   poetry add pytest-loco-http

To work with JSON payloads, add the JSON extension:

.. code-block:: console
   :caption: Add the JSON extension for working with JSON payloads

   poetry add pytest-loco-json

Configure IDE
-------------

``pytest-loco`` provides a command to configure VSCode's
`YAML Language Support <https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml>`_
by Red Hat for schema validation and autocompletion inside your test files.

Make sure the **YAML Language Support** extension is installed in VSCode, then run:

.. code-block:: console
   :caption: Configure VSCode YAML Language Support for pytest-loco

   poetry run pytest-loco vscode-configure

This generates the necessary VSCode workspace settings so that the editor
recognises the pytest-loco DSL schema and provides inline validation and
suggestions as you edit ``test_*.yaml`` test files.

----

Create a first test case
------------------------

``pytest-loco`` collects YAML files whose names match the pattern ``test_*.yml`` or ``test_*.yaml``.
Any such file found under the configured test paths is treated as a DSL specification and executed as a test.

Place test files in your ``tests/`` directory (or any path passed to pytest) and name them accordingly:

.. code-block:: text
   :caption: Example test files structure

   tests/
   ├── test_user.yaml
   ├── test_items.yaml
   └── utils/
       └── auth.yaml

A test case is a YAML file containing documents separated by ``---``:

1. The **case document** - declares the test metadata, variables, and environment bindings.
2. One or more **step documents** - describe the actions to execute and the expectations to assert.

Create the file ``tests/test_hello_world.yaml``:

.. code-block:: yaml
   :caption: Example test case in YAML format

   ---
   spec: case
   title: Hello World
   description: >
     Verify that a simple variable can be set and checked.
   vars:
     greeting: Hello, World!

   ---

   title: Check greeting value
   action: empty
   vars:
     expected: !var greeting
   export:
     actual: !var expected
   expect:
     - title: Greeting matches expected value
       value: !var actual
       match: Hello, World!

Run the test case
-----------------

Use pytest to discover and run the test:

.. code-block:: console
   :caption: Run the test case with pytest

   poetry run pytest tests/test_hello_world.yaml -v

``pytest-loco`` registers a pytest plugin that collects ``test_*.yaml`` case files automatically.

To run all test cases in the ``tests/`` directory:

.. code-block:: console
   :caption: Run all test cases in the tests/ directory

   poetry run pytest tests/ -v
