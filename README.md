# Text To Speech POC

This is a simple POC to test the Text To Speech functionality in Python.

## Installation

```bash
pip install -r requirements.txt -U
```

## Usage

### Terminal

```bash
source .venv/bin/activate
py src/main.py
```

### IDE

Load Python Environment via the command pallette, and then use the debug option to run the `main.py` file.

## Troubleshooting

### SSL issues

Make sure you've configured your PIP SSL settings properly. You can do this by running the following command:

```bash
pip config set global.trusted-host \
    "pypi.org files.pythonhosted.org pypi.python.org" \
    --trusted-host=pypi.python.org \
    --trusted-host=pypi.org \
    --trusted-host=files.pythonhosted.org
```
