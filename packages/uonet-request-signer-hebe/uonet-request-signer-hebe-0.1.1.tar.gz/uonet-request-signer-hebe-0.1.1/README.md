# UONET+ (hebe) request signer for Python

[![pypi](https://img.shields.io/pypi/v/uonet-request-signer-hebe.svg?style=flat-square)](https://pypi.org/project/uonet-request-signer-hebe/)

## Installation

```console
$ pip install -U uonet-request-signer-hebe
```

## Usage

Generate an RSA2048 key pair (private key and certificate):
```python
from uonet_request_signer_hebe import generate_key_pair

certificate, fingerprint, private_key = generate_key_pair()
```

Sign request content:
```python
from uonet_request_signer_hebe import get_signature_values
from datetime import datetime

digest, canonical_url, signature = get_signature_values(fingerprint, private_key, body, full_url, datetime.now())
```

## Tests

```console
$ python -m pytest .
```
