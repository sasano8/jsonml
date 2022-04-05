# jsonml
<!--
[![Version](https://img.shields.io/pypi/v/asy)](https://pypi.org/project/asy)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
-->

This library is a python implementation of jsonml.

See below for jsonml specifications.

- http://www.jsonml.org/

# Requirement

- Python 3.8+


# Getting Started

``` python
from jsonml import Parser

parser = Parser()

obj = ["tag1", ["tag2", ["tag3", "1"]]]

tree_1 = parser.parse_from_obj(obj)
xml_1 = parser.to_xml(tree_1)
jsonml = parser.to_jsonml(tree_1)

tree_2 = parser.parse_from_xml_string(xml_1)
assert parser.to_jsonml(tree_2) == jsonml
```


```
<tag1><tag2><tag3>1</tag3></tag2></tag1>
```

```
[
  "tag1",
  [
    "tag2",
    [
      "tag3",
      "1"
    ]
  ]
]
```


# Contribute

```
poetry install
pre-commit install
source .venv/bin/activate
make
```
