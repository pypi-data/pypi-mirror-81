# dbnomics-fetcher-toolbox

Toolbox of functions and data types helping writing DBnomics fetchers.

[![Documentation Status](https://readthedocs.org/projects/dbnomics-fetcher-toolbox/badge/?version=latest)](https://dbnomics-fetcher-toolbox.readthedocs.io/en/latest/?badge=latest)

## Installation

If you're using this package, you may be working on a DBnomics fetcher.
In that case, just add the `dbnomics-fetcher-toolbox` package to your requirements file.

Example using [pip-tools](https://github.com/jazzband/pip-tools) in a Python [virtual environment](https://docs.python.org/3/library/venv.html).

```bash
# Create a Python virtual environment
python -m venv my-fetcher

# Activate the virtual environment
source my-fetcher/bin/activate

# Install dependencies management tool
pip install pip-tools

# Declare dependency
echo dbnomics-fetcher-toolbox >> requirements.in

# Freeze dependencies
pip-compile

# Synchronize the virtual environment with frozen dependencies
pip-sync
```

Note: this workflow is quite complex due to the Python ecosystem which does not define a standard way to manage dependencies.
You can use another packaging tool like [poetry](https://python-poetry.org/).

## Documentation

See https://dbnomics-fetcher-toolbox.readthedocs.io/

## Contributing

### Documentation

To contribute to the documentation, install:

```
pip install --editable .[doc]
pip install sphinx-autobuild
```

Then launch:

```
sphinx-autobuild --watch dbnomics_fetcher_toolbox doc doc/_build/html
```
