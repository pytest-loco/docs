:tocdepth: 2

Format
======

Content basics
--------------

Working with content is a fundamental aspect of the DSL, and the
framework provides built-in support for handling various content formats.
The ``!load`` and ``!dump`` features enable seamless decoding and encoding
of content, allowing users to easily transform data between different
representations.

By default, content instructions support ``format`` parameter that specify
the content type and ``source`` parameter that indicates the value to be processed.
The framework does not include built-in support for any specific content formats,
but they can be extended with plugins, such as the JSON format provided by
the ``pytest-loco-json`` plugin.

.. rubric:: Base input schema

.. autopydantic_model:: schemas.Content
   :model-signature-prefix: entity
   :field-signature-prefix: param


Decoders
--------

Decoding content is achieved using the ``!load`` feature, which takes the
specified format and source, and transforms the content into a structured data
representation that can be easily manipulated within the DSL.

Decoders can contain optional transformers that allow users to interact with
specific data from the decoded content. This feature is particularly useful when
working with complex data structures, as it enables users to focus on the relevant
parts of the content without having to navigate through the entire structure.

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

Encoders
--------

Encoding content is achieved using the ``!dump`` feature, which takes a structured
data representation from the execution context and transforms it into a specific
format that can be easily consumed by external systems or stored for later use.

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
