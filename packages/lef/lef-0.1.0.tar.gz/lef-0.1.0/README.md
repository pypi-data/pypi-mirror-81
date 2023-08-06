# Python Extension Framework

This is a framework for building [AWS Lambda Extensions](https://aws.amazon.com/blogs/compute/introducing-aws-lambda-extensions-in-preview/).

## Quickstart

```bash
$ pip install lef
```

To get started you can use the default `Extension` class, or extend it.

Example:

```python
from lef import Extension

def handler(event):
    print(event)

extension = Extension()
extension.register([EventType.INVOKE], handler)
```
