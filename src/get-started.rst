Get Started
===========

Manual setup
------------

Create a project
~~~~~~~~~~~~~~~~

**Prerequisites**: Python and
`Poetry <https://python-poetry.org/docs/#installation>`_
must be installed.

Create a new Poetry project and add pytest-loco as a dependency:

.. code-block:: console
   :caption: Create a new Poetry project and add pytest-loco

   poetry new example-project
   cd example-project
   poetry add pytest-loco

Create a test case
~~~~~~~~~~~~~~~~~~~

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

Run the tests
~~~~~~~~~~~~~

Use pytest to discover and run the test:

.. code-block:: console
   :caption: Run the test case with pytest

   poetry run pytest

``pytest-loco`` registers a pytest plugin that collects case files automatically.


Boilerplating
-------------

You can simplify the process by using a boilerplate, such as an API testing boilerplate.

Create a project
~~~~~~~~~~~~~~~~

**Prerequisites**: Python,
`Cookiecutter <https://cookiecutter.readthedocs.io/en/stable/installation.html>`_ and
`Poetry <https://python-poetry.org/docs/#installation>`_
must be installed.

Create a project from the repo template:

.. code-block:: console
   :caption: Create a new Poetry project from a boilerplate

   cookiecutter https://github.com/pytest-loco/api-tests.git

Follow the instructions provided by Cookiecutter.

Run the tests
~~~~~~~~~~~~~

Use pytest to discover and run the test:

.. code-block:: console
   :caption: Run the test case with pytest

   poetry run pytest

See ``README.md`` in the new project's root for more details.
