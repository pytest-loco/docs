:tocdepth: 2

Case
====

Definition
----------

A case represents a runnable test scenario. It is defined in a YAML document
with the ``spec`` field set to ``case``. After the case, you can define any number
of nested steps, which are executed sequentially. Cases can also include metadata
and variables that are accessible within the execution context.

.. code-block:: yaml
   :caption: Case definition example

   spec: case
   title: Short human-readable case title
   description: >
     Detailed human-readable description of the scenario.
     May span multiple lines and is intended for documentation
     and reporting purposes
   metadata:
     tags:
     - engine
     - example
   vars:
     baseUrl: https://httpbin.org

Only documents under a case are executed.

.. rubric:: Input schema

.. autopydantic_model:: schemas.Case
   :model-signature-prefix: entity
   :field-signature-prefix: param

Environment
-----------

You can use the ``envs`` field to define environment variables that will be set
during the execution of the case. These variables are accessible to all steps within
the case and can be used to configure the execution environment.

.. code-block:: yaml
   :caption: Environment variables example

   ---
   spec: case
   title: Case with environment variables
   vars:
     baseUrl: https://httpbin.org
   envs:
   - name: API_KEY
     description: API key for authentication
     required: yes
     secret: yes

   ---
   title: Example of accessing environment variable in a step
   action: http.get
   url: !var baseUrl
   headers:
     x-api-token: !secret envs.API_KEY

.. rubric:: Input schema

.. autopydantic_model:: schemas.InputDefinition
   :model-signature-prefix: entity
   :field-signature-prefix: param

Only simple types are supported as environment variable values:

.. autotype:: schemas.TypeName

Parametrize
-----------

Case can be parameterized using the ``params`` field. This allows you to
define variables that can be used within the case and its steps, enabling
dynamic and flexible test scenarios.

On definition of several values for a parameter, the case will be executed
once for each value, allowing you to easily test different scenarios without
duplicating the case definition. On definition of several parameters with
several values, the case will be executed for each combination of parameter values.

.. code-block:: yaml
   :caption: Case parameterization example

   ---
   spec: case
   title: Parameterized case example
   params:
   - title: The API url to use for the request
     name: apiUrl
     values:
     - https://httpbin.org/ip
     - https://httpbin.org/user-agent
     - https://httpbin.org/headers

   ---
   title: Example of accessing case parameter in a step
   action: http.get
   url: !var params.apiUrl

.. rubric:: Input schema

.. autopydantic_model:: schemas.Parameter
   :model-signature-prefix: entity
   :field-signature-prefix: param
