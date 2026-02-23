Instructions
============

JSONPath querying
-----------------

.. seealso::

   `Python JSONPath Documentation <https://jg-rp.github.io/python-jsonpath/syntax/>`_
      This guide introduces the standard JSONPath syntax and explains the non-standard
      extensions and their semantics.

   `JSONPath RFC <https://datatracker.ietf.org/doc/html/rfc9535>`_
      RFC 9535 defines a string syntax for selecting and extracting JSON values
      from within a given JSON value.

Provide ``!jsonpath`` instruction that allow querying by JSONPath expressions
defined directly inside the DSL. Queries are compiled during schema loading.
This ensures that invalid JSONPath syntax is detected immediately before the
scenario starts, providing early error reporting.

.. code-block:: yaml
   :caption: Syntax

   !jsonpath <variable> <jsonpath-query>

* ``<variable>`` - path to a context variable containing a JSON value
* ``<jsonpath-query>`` - JSONPath expression

Both parts must be separated by whitespace.

Also you can use the special symbols:

* ``@`` refers to the current element in the JSONPath iteration
* ``_`` refers to the global context, allowing you to filter data based on other variables

.. code-block:: yaml
   :caption: Example

   ---
   title: Create object for querying
   action: empty

   export:
     ageLimit: 30
     persons:
     - name: Molecule Man
       age: 29
       powers:
       - Radiation resistance
       - Turning tiny
       - Radiation blast
     - name: Madame Uppercut
       age: 39
       powers:
       - Million tonne punch
       - Damage resistance
       - Superhuman reflexes

   ---
   title: Select from object
   action: empty

   export:
     powers: !jsonpath persons $[?(@.age<_.ageLimit)].powers[*]

   expect:

   - title: Check that result is list of powers
     value: !var powers
     match:
     - Radiation resistance
     - Turning tiny
     - Radiation blast

The result is always a list.
