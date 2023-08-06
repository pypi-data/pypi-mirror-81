# UONET+ (hebe) request signer for Python

[![pypi](https://img.shields.io/pypi/v/uonet-request-signer-hebe.svg?style=flat-square)](https://pypi.org/project/uonet-request-signer-hebe/)

## Installation

```console
$ pip install -U uonet-request-signer-hebe
```

## Usage

```python
from uonet_request_signer_hebe import get_signature_values
from datetime import datetime

digest, canonical_url, signature = get_signature_values(fingerprint, private_key, body, full_url, datetime.now())
```

## Tests

```console
$ python -m pytest .
```
