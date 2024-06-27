# Text To Speech POC

This is a simple POC to test the Text To Speech functionality in Python.

## Model

This POC is using the [`speecht5_tts`](https://huggingface.co/microsoft/speecht5_tts) Model, by Microsoft.

<!-- Another model we support is the [`blabble-io/libritts_r`](https://huggingface.co/datasets/blabble-io/libritts_r) model. -->

## Installation

```bash
pip install -r requirements.txt -U
```

Add the following Env variables to your `.env` file:

```bash
HUGGINGFACEHUB_API_TOKEN=<YOUR_TOKEN>
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
