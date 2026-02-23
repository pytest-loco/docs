Instructions
============

URL construction
----------------

Provide ``!urljoin`` instruction that compose a URL at runtime by joining
a base URL from the DSL context with a postfix path.

This instruction is useful when endpoints depend on previously resolved
values (e.g. environment-specific base URLs, dynamically returned URLs,
or configuration variables).

.. code-block:: yaml
   :caption: Syntax

   !urljoin <variable> <postfix>

* ``<variable>`` - path for a context variable containing a base URL
* ``<postfix>`` - relative path segment to append to the base URL

Both parts must be separated by whitespace.

.. code-block:: yaml
   :caption: Example

   action: http.get
   vars:
     baseUrl: https://api.example.com
   url: !urljoin baseUrl api/v1/users

Resulting URL at runtime: ``https://api.example.com/api/v1/users``.
