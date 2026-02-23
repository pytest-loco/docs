VSCode
======

To enhance your development workflow, this package integrates into
`VSCode <https://code.visualstudio.com/>`_ using the
`YAML Language Support by Red Hat <https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml>`_
extension. A dedicated DSL schema is provided, allowing the extension
to perform real-time validation and offer IntelliSense hints while you work.

Configuration
-------------

Running this command at the project root generates a schema including all
installed ``pytest-loco`` extensions in the ``.vscode`` directory and automatically
configures the necessary validation options in ``settings.json``:

.. tab:: User

   .. code-block:: console
      :caption: Configure integration

      pytest-loco vscode-configure

.. tab:: Poetry Project

   .. code-block:: console
      :caption: Configure integration

      poetry run pytest-loco vscode-configure
