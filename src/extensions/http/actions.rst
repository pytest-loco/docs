:tocdepth: 2

Actions
=======

The following methods are available as actions: ``http.connect``,
``http.delete``, ``http.get``, ``http.head``, ``http.options``,
``http.patch``, ``http.post``, ``http.put`` and ``http.trace``.

Basics
------

.. rubric:: Query

Query parameters can be passed using the ``params`` field.

.. code-block:: yaml
   :caption: Make request with query parameters

   title: Make request with query parameters
   description: Send query parameters by HTTP GET

   action: http.get

   url: https://httpbin.org/get
   params:
     test: 'true'


Query parameters are automatically encoded and appended to the URL.

.. rubric:: Data

The ``data`` field allows sending raw request bodies as ``str`` or ``bytes``.

.. code-block:: yaml
   :caption: Make request with data

   title: Make request with data
   description: Send JSON by HTTP POST

   action: http.post

   url: https://httpbin.org/post
   headers:
     content-type: application/json
   data: '{"message": "hello", "test": true}'

The raw body is preserved in the response model as:

* ``request.body`` as bytes
* ``request.text`` as text

.. rubric:: Files

Multipart file uploads are supported via the files field.

Each file entry defines:

* ``name`` - form field name
* ``content`` - string or bytes
* ``filename`` (optional)
* ``mimetype`` (optional)

If ``mimetype`` is not provided, it is inferred:

* ``application/octet-stream`` for bytes
* ``text/plain`` for strings

.. rubric:: Binary file

.. code-block:: yaml
   :caption: Make request with binary file

   title: Make request with binary file
   description: >
     1. Get binary data from hex
     2. Send binary attachment by HTTP POST

   action: http.post

   url: https://httpbin.org/post
   files:
   - name: test
     content: !binaryHex |
       48 65 6C 6C 6F 2C 20
       57 6F 72 6C 64 21

.. rubric:: Text file

.. code-block:: yaml
   :caption: Make request with text file

   title: Make request with text file
   description: >
     1. Get text data from file
     2. Send text attachment by HTTP POST

   action: http.post

   url: https://httpbin.org/post
   files:
   - name: test
     content: !textFile example.txt

Inputs
------

.. rubric:: Input schemas

All methods share an identical base parameter structure, differing
only in the allowed values for the ``action`` field and the specifics
of request body processing. The structure below is shown for one action,
but it serves as a reference for all other HTTP actions.

.. rubric:: Action schema

.. autopydantic_model:: schemas.http.HttpGet
   :model-signature-prefix: action
   :field-signature-prefix: param

.. rubric:: Nested schemas

Files represented as nested structured objects with ``name`` and 
``content`` fields.

.. autopydantic_model:: schemas.http.File
   :model-signature-prefix: object


Outputs
-------

.. rubric:: Output schemas

Every method generates a :class:`~schemas.http.Response`
object at the output.

Response fields include:

* ``status`` - HTTP status
* ``headers`` - normalized response headers (lowercase keys)
* ``cookies`` - list of structured cookies
* ``body`` - raw response body (bytes)
* ``text`` - response body as text
* ``request`` - structured original request
* ``history`` - redirect chain (list of responses)

.. autopydantic_model:: schemas.http.Response
   :model-signature-prefix: object

Redirect history can be inspected:

.. code-block:: yaml
   :caption: Get response with redirects

   title: Test redirects history
   description: >
     This test verifies that a GET request to the /redirect-to endpoint with a URL
     parameter that points to a /status/204 endpoint returns a status code of 204
     and that the response history includes a redirect with a status code of 302.

   action: http.get
   url: !urljoin baseUrl /redirect-to
   params:
     url: !urljoin baseUrl /status/204
   headers:
     accept: application/json

   output: response

   expect:

   - title: Status is 204
     value: !var response.status
     match: 204

   - title: History is not empty
     value: !var response.history
     notEqual: []

   - title: Status of redirect response is 302
     value: !var response.history.0.status
     match: 302

.. rubric:: Nested schemas

The original HTTP request is provided as a nested object.

.. autopydantic_model:: schemas.http.Request
   :model-signature-prefix: object

Cookies from the response are provided as nested structured objects
with secret values.

.. autopydantic_model:: schemas.http.Cookie
   :model-signature-prefix: object

The parsed URL is provided as a nested structure, broken down into
its components.

.. autopydantic_model:: schemas.http.Url
   :model-signature-prefix: object


Examples
--------

.. rubric:: HTTP GET

This scenario demonstrates a basic ``http.get`` action. It performs an HTTP GET
request to a URL formed by joining a base URL with the ``/get`` path. The request
includes a custom accept header and query parameter ``test``. After execution, the
result is stored in the ``response`` variable. Finally, two expectations are validated:
the HTTP status code must be ``200``, and the response body must contain a specific
echo message verified via a multiline regular expression.

.. code-block:: yaml
   :caption: http.get

   title: Test GET
   description: >
     This test verifies that a GET request to the /get endpoint returns a status
     code of 200 and that the response contains the correct URL from the request.

   action: http.get
   url: !urljoin baseUrl /get
   headers:
     accept: application/json

   output: response

   expect:

   - title: Status is 200
     value: !var response.status
     match: 200

   - title: Response contains request URL
     description: >
       The response should include the URL that was requested, confirming that
       the server received the correct request and is returning the expected
       data in the response.
     value: !load
       format: json
       source: !var response.text
       select: $.url
     match: https://httpbin.org/get

.. rubric:: HTTP POST with files

This scenario demonstrates an ``http.post`` action with a multipart file upload.
It performs an HTTP POST request to a dynamically constructed URL. The request includes
a custom accept header and a text file named test with the content ``Hello, World!``.
The action output is stored in the ``response`` variable. Finally, the scenario validates
that the server returned a ``200`` status and that the response body contains the uploaded
file data, verified via a multiline regular expression.

.. code-block:: yaml
   :caption: http.post

   title: Test POST with text file
   description: >
     This test verifies that a POST request to the /post endpoint with a text file
     returns a status code of 200 and that the response contains the correct file
     content that was sent in the request.

   action: http.post
   url: !urljoin baseUrl /post
   headers:
     accept: application/json
   files:
   - name: test
     content: Hello, World!

   output: response

   expect:

   - title: Status is 200
     value: !var response.status
     match: 200

   - title: Body was sent
     description: >
        The response should include the content of the file that was sent in the
        request, confirming that the server received the file correctly and is
        returning the expected data in the response.
     value: !load
       format: json
       source: !var response.text
       select: $.files
     match:
       test: Hello, World!

.. rubric:: HTTP PATCH with JSON

This scenario demonstrates an ``http.patch`` action with a JSON payload.
It performs an HTTP PATCH request with a dynamically constructed URL. The request includes
a structured JSON body generated from a source object via the ``!dump`` instruction.
After execution, the response text is parsed back into a JSON object using the ``!load``
instruction and exported as the ``responseMessage`` variable. The scenario concludes
by validating a ``200`` status and performing a partial match to verify that the sent data
was correctly processed by the server.

.. code-block:: yaml
   :caption: http.patch

   title: Test PATCH with JSON content
   description: >
     This test verifies that a PATCH request to the /patch endpoint with JSON content
     returns a status code of 200 and that the response contains the correct JSON
     data that was sent in the request.

   vars:
     requestData: !dump
       format: json
       source:
         name: Molecule Man
         age: 29
         secretIdentity: Dan Jukes
         powers:
         - Radiation resistance
         - Turning tiny
         - Radiation blast

   action: http.patch
   url: !urljoin baseUrl /patch
   headers:
     accept: application/json
     content-type: application/json
   data: !var requestData

   output: response

   expect:

   - title: Status is 200
     value: !var response.status
     match: 200

   - title: Body was sent
     description: >
       The response should include the JSON data that was sent in the request, confirming
       that the server received the correct data and is returning the expected
       information in the response.
     value: !load
       format: json
       source: !var response.text
       select: $.json
     partialMatch: yes
     match:
       name: Molecule Man
       age: 29
