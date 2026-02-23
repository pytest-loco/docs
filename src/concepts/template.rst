:tocdepth: 2

Template
========

Definition
----------

A template defines reusable logic that can be applied to multiple cases.

Templates are defined in YAML files with the ``spec`` field set to ``template``.
They can be stored in any location and organized as needed. Templates are resolved
at parse time and merged into the execution graph, allowing them to be invoked from
cases or other templates using the ``include`` action.

.. code-block:: yaml
   :caption: Template definition example

   spec: template
   title: Short human-readable template title
   description: >
     Detailed human-readable description of the scenario template.
     May span multiple lines and is intended for documentation
     and reporting purposes
   params:
   - name: baseUrl
     type: string
     default: https://httpbin.org

Templates allow reuse of common workflows and logic across multiple cases, promoting
modularity and maintainability in test design. By defining a template once and invoking it
from multiple cases, you can avoid duplication and ensure consistency in your test scenarios.

.. rubric:: Input schema

.. autopydantic_model:: schemas.Template
   :model-signature-prefix: entity
   :field-signature-prefix: param

Inclusion
---------

A template can be invoked from a case or another template using the
``include`` action. The caller may pass variables into the action context
via ``vars``. These variables are treated as parameters of the invoked template.

The template execution context is isolated: only values explicitly declared as
template parameters are transferred and shared. This allows templates to be reused
in different contexts without unintended side effects, as they do not have access
to the caller's variables unless explicitly passed as parameters.

.. code-block:: yaml
   :caption: Template inclusion example

   title: Example of invoking the template from a case
   description: >
     This step demonstrates how a template can be invoked from
     within a case using the `include` action. The caller may pass
     variables into the action context via `vars`. These variables
     are treated as parameters of the invoked template. The template
     execution context is isolated: only values explicitly declared
     as template parameters are transferred and shared.
   action: include
   vars:
     argument: OK
   file: echo.yaml
   export:
     value: !var result.value
   expect:
   - title: Value exists in include result
     value: !var value
     match: OK

.. rubric:: Input schema

.. autopydantic_model:: schemas.IncludeAction
   :model-signature-prefix: action
   :field-signature-prefix: param
