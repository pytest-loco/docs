Allure
======

pytest-loco-allure
------------------

The ``pytest-loco-allure`` extension adds the Allure reports collection. The extension
acts as a bridge between your test DSL and the Allure reporting engine. By defining the
``metadata`` dictionary within your test case, you can control how the results are visualized
in the Allure report without calling Allure APIs manually.

By default, using ``title`` and ``description`` fields for annotating.

Installation
------------

Requires Python 3.13 or newer.

.. tab:: User

   .. code-block:: console
      :caption: Install from PyPI 

      pip install pytest-loco-allure[markdown]

.. tab:: Poetry Project

   .. code-block:: console
      :caption: Install from PyPI 

      poetry add pytest-loco-allure[markdown]

The description field optionally supports Markdown formatting, allowing you to include
rich text, lists, and tables directly in the Allure report body.

Usage
-----

.. seealso::

   `Allure Pytest <https://allurereport.org/docs/pytest/>`_
      Getting started with Allure Pytest

Run your tests as you would do normally.

Generate the HTML report by using Allure CLI command:

.. code-block:: console
   :caption: Generate the HTML report

   allure generate --single-file --clean

The ``metadata`` dictionary within the Case-spec serves as a centralized configuration
layer that maps high-level test definitions directly to Allure's reporting structure.
Instead of manual instrumentation, the extension automatically extracts these attributes
during the test setup phase and populates the Allure lifecycle, ensuring your reports
reflect the intended business logic and hierarchy.

The following fields are supported within the Case-spec metadata:

* **Categorization**: ``epic``, ``feature``, and ``story`` - define the behavioral hierarchy
* **Organization**: ``parent``, ``suite`` - override the default file-system grouping
* **Information**: ``id`` and ``severity`` - provide the Allure TestOps ID and indicate the priority
* **References**: ``tags``, ``issues`` and ``links``
