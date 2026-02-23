:tocdepth: 2

Step
====

Definition
-----------

A step is a single unit of work that can be executed as part of a test.
It is defined in a YAML document with the ``spec`` field set to ``step``
(not required by default). A step can represent an action to perform
and a sequence of checks to validate.

At runtime:

* The core locates the plugin that registered this action
* The action schema is validated
* Arguments are parsed and compiled (including deferred expressions)
* The plugin executes the action implementation

.. code-block:: yaml
   :caption: Step definition example

   title: Short human-readable step title
   description: >
     Detailed human-readable description of the step.
     May span multiple lines and is intended for documentation
     and reporting purposes
   action: empty

   vars:
     expectedValue: Hello, world!
   export:
     actualValue: !var expectedValue

   expect:

   - title: Check that value is correct
     value: !var actualValue
     match: !var expectedValue

After execution, the action produces a result object. By convention, this result
is stored in the case context under ``result``. But user can redefine output
variable name by ``output`` field.

The step definition can include an optional ``vars`` section, which allows
you to define local variables that will be added to the execution context
before the step is executed. These variables can then be accessed within the
step using the ``!var`` syntax.

The step definition can include an optional ``export`` section, which allows
you to define variables that will be added to the global execution context after
the step is executed. These variables can then be accessed in next steps using
the ``!var`` syntax.

Export:

* Evaluates expressions after action execution
* Stores values in case context
* Makes them available to next steps

.. rubric:: Base input schema

.. autopydantic_model:: schemas.Action
   :model-signature-prefix: entity
   :field-signature-prefix: param

By default, the core provides a single action called ``empty``, which does nothing.
You can use core extension mechanism to define your own actions and make them available
in steps. This allows you to extend the functionality of steps and reuse common actions
across different steps and tests.

Expectations
------------

Expectations are defined in the ``expect`` field of a step. They represent
assertions that must hold true for the step to be considered successful. Each
expectation can have an optional title for better reporting and documentation.
Expectations can reference variables defined in the step or in the global context.

Expectations:

* Are evaluated after export
* Operate on fully resolved values
* Produce structured assertion results
* Are reported individually
* Failure of an expectation fails the step and the case

.. rubric:: Base input schema

.. autopydantic_model:: schemas.Check
   :model-signature-prefix: entity
   :field-signature-prefix: param

Expectations can be extended by plugins.

Builtins
--------

Match
~~~~~

Match check validates that the value matches the expected value.
The check can be used to compare values of any type, including strings,
numbers, lists, and dictionaries. The check performs a deep comparison,
meaning that it will compare the contents of lists and dictionaries
rather than just their references.

For partial matching of list or dictionaries, you can use the ``partialMatch``
check, which allows you to specify only a subset of the expected values.
The check will validate that the actual list or dictionary contains at least
the specified values, while ignoring any additional keys.

.. code-block:: yaml
   :caption: Partial match example

   expect:

   - title: Check that actual value contains expected values
     match:
       name: Bob Plissken
       age: 35
     partialMatch: yes
     value:
       name: Bob Plissken
       age: 35
       city: New York

.. rubric:: Input schemas

.. autopydantic_model:: schemas.MatchCheck
   :model-signature-prefix: entity
   :field-signature-prefix: param

.. autopydantic_model:: schemas.NotMatchCheck
   :model-signature-prefix: entity
   :field-signature-prefix: param

Comparison
~~~~~~~~~~

Comparison checks allow you to compare values using standard comparison
operators such as greater than, less than, etc. These checks can be used to
validate that a value meets certain criteria, such as being greater than a
specified threshold or less than a maximum value. Comparison checks can be
applied to numeric values, strings and other comparable types.

.. code-block:: yaml
   :caption: Comparison check example

   expect:

   - title: Check that actual value is greater than expected value
     greaterThan: 10
     value: 15

.. rubric:: Input schemas

.. autopydantic_model:: schemas.GreaterThanCheck
   :model-signature-prefix: entity
   :field-signature-prefix: param

.. autopydantic_model:: schemas.GreaterThanOrEqualCheck
   :model-signature-prefix: entity
   :field-signature-prefix: param

.. autopydantic_model:: schemas.LessThanCheck
   :model-signature-prefix: entity
   :field-signature-prefix: param

.. autopydantic_model:: schemas.LessThanOrEqualCheck
   :model-signature-prefix: entity
   :field-signature-prefix: param

Regular expression
~~~~~~~~~~~~~~~~~~

.. seealso::

   `Python Regular expressions <https://docs.python.org/3/library/re.html>`_
      This module provides regular expression matching operations similar to those found in Perl.

Regular expression checks allow you to validate that a string value matches
a specified regular expression pattern. These checks can be used to ensure
that a value conforms to a specific format, such as an email address, phone number,
or any custom pattern defined by the user. Regular expression checks can be applied
to string values and provide a powerful way to validate complex patterns and formats.

.. code-block:: yaml
   :caption: Regular expression check example

   expect:
   - title: Check that actual value matches regular expression pattern
     regex: '^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,5}$'
     ignoreCase: yes
     value: !var emailAddress

.. rubric:: Input schemas

.. autopydantic_model:: schemas.RegexCheck
   :model-signature-prefix: entity
   :field-signature-prefix: param
