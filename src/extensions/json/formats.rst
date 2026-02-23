:tocdepth: 2

Formats
=======

Decoders
--------

The ``!load`` feature can parse a JSON string into native Python objects and
stores them as values in the execution context. Decoding allows JSON payloads
to become fully addressable within the DSL execution context. Once decoded,
values can be inspected, exported, validated, or transformed by subsequent steps.

Decoder parameters are intentionally minimal: decoding focuses on
correctness and performance, while transformation logic is handled
separately.

For example:

.. code-block:: yaml
   :caption: Example of decoding a value

   ---
   title: Read a JSON content from file
   action: empty
   export:
     jsonText: !textFile test.json

   ---
   title: Decode a JSON
   action: empty
   export:
     jsonValue: !load
       format: json
       source: !var jsonText

The result of executing this case will be the assignment of the decoded
object to the variable.

.. rubric:: Input schemas

.. autopydantic_model:: schemas.json.Decoder
   :model-signature-prefix: entity
   :field-signature-prefix: param


Encoders
--------

The ``!dump`` feature serializes a value from the execution context into a
JSON string using the high-performance ``orjson`` backend.

Encoding is typically used when preparing request payloads, exporting
structured data, or normalizing values for comparison. The encoder
accepts an optional ``sortKeys`` parameter that controls serialization
behavior and enables deterministic key ordering. Encoded values are returned
as UTF-8 strings and can be passed directly to actions (for example, HTTP
requests) or stored in the execution context.

For example:

.. code-block:: yaml
   :caption: Example of encoding a value

   ---
   spec: case
   title: Example of encoding a value
   vars:
     value:
       name: Molecule Man
       secretIdentity: Dan Jukes
       age: 29

   ---
   action: empty
   export:
     jsonText: !dump
       format: json
       source: !var value

The result of executing this case will be the assignment of the
following JSON string to the variable (shown here formatted for readability):

.. code-block:: json
   :caption: Example result

   {
     "name": "Molecule Man",
     "age": 29,
     "secretIdentity": "Dan Jukes"
   }

Optionally, you can use the ``sortKeys`` option, in this case, the
keys will be sorted alphabetically:

.. code-block:: json
   :caption: Example result with sorted keys

   {
     "age": 29,
     "name": "Molecule Man",
     "secretIdentity": "Dan Jukes"
   }

.. rubric:: Input schemas

.. autopydantic_model:: schemas.json.Encoder
   :model-signature-prefix: entity
   :field-signature-prefix: param


Transforms
----------

The ``!load`` feature can be extended with an optional transformer that
enables extracting data from decoded JSON structures using JSONPath
expressions.

.. seealso::

   `Python JSONPath Documentation <https://jg-rp.github.io/python-jsonpath/syntax/>`_
      This guide introduces the standard JSONPath syntax and explains the non-standard
      extensions and their semantics.

   `JSONPath RFC <https://datatracker.ietf.org/doc/html/rfc9535>`_
      RFC 9535 defines a string syntax for selecting and extracting JSON values
      from within a given JSON value.

Transforms are applied after decoding and allow selecting either a
single value or multiple values from complex, deeply nested documents.
Behavior is configurable to return the first match, the last match, or
a full list of matches. This makes it possible to work with large or variable
JSON payloads without hard-coding structural assumptions into the test logic.

Use the following ``test.json`` file contents as an example:

.. code-block:: json
   :caption: Data for testing JSONPath querying

   [
     {
       "name": "Molecule Man",
       "age": 29,
       "secretIdentity": "Dan Jukes",
       "powers": [
         "Radiation resistance",
         "Turning tiny",
         "Radiation blast"
       ]
     },
     {
       "name": "Madame Uppercut",
       "age": 39,
       "secretIdentity": "Jane Wilson",
       "powers": [
         "Million tonne punch",
         "Damage resistance",
         "Superhuman reflexes"
       ]
     }
   ]

Optionally, you can use the ``query`` transformer with ``!load``:

.. code-block:: yaml
   :caption: Example of transforming a value

   title: Decode JSON and select the first match
   action: empty

   export:
     jsonValue: !load
       format: json
       source: !var jsonText
       query: '$[*].name'

   expect:

   - title: Check first selected name
     value: !var jsonValue
     match: Molecule Man

By default, the first match of the JSONPath query is selected.
This behavior can be controlled using the ``exactOne`` parameter
(``true`` or ``false``; when ``false``, the query returns a full list of
matches) and the ``exactMode`` parameter (``first`` or ``last`` on a
single mode querying).

For example:

.. code-block:: yaml
   :caption: Example of transforming a value

   title: Decode JSON and select all matches
   action: empty

   export:
     jsonValues: !load
       format: json
       source: !var jsonText
       query: '$[?(@.age<30)].powers[*]'
       exactOne: no

   expect:

   - title: Check that result is list of powers
     value: !var jsonValues
     match:
     - Radiation resistance
     - Turning tiny
     - Radiation blast

.. rubric:: Input schemas

.. autopydantic_model:: schemas.json.SelectiveDecoder
   :model-signature-prefix: entity
   :field-signature-prefix: param
