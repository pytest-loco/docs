# Documentation

Created with [Sphinx](https://www.sphinx-doc.org/en/master/).

## How to build HTML

**Prerequisites:** [Poetry](https://python-poetry.org/) must be installed.

1. Install dependencies:
   ```sh
   poetry install
   ```

2. Build the HTML docs:
   ```sh
   make clean && make html
   ```

3. Open the output in your browser:
   ```
   _build/html/index.html
   ```
