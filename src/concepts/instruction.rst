:tocdepth: 2

Instruction
===========

Instructions are the fundamental building blocks of the DSL, representing
individual steps or actions that can be executed within a test case.
Each instruction is defined by its type (for example, ``!load`` or ``!dump``)
and can include scalar value or various parameters as mapping that specify
its behavior and the data it operates on.

Instructions are realized as YAML tags, which allows them to be easily identified
and processed by the DSL execution engine. The framework provides a set of
built-in instructions, and users can also define custom instructions through
plugins to extend the functionality of the DSL.

Builtins
--------

The built-in instructions include:

* ``!var <variable path>``: Retrieves the value of a variable from the execution context
* ``!secret <variable path>``: Retrieves the value of a secret variable from the execution context
* ``!date <date string>``: Parses a date string into a date object
* ``!datetime <datetime string>``: Parses a datetime string into a datetime object
* ``!timedelta <seconds>``: Parses a seconds value into a timedelta object
* ``!duration <duration string>``: Parses a duration string into a timedelta object
* ``!binaryFile <file path>``: Reads a binary file and returns its content as bytes
* ``!textFile <file path>``: Reads a text file and returns its content as a string
* ``!binaryHex <hex string>``: Parses a hexadecimal string into bytes
* ``!base64 <base64 string>``: Parses a base64-encoded string into bytes
