OARepo Invenio data model
=========================

[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]

Invenio base record model.

Instalation
----------
```bash
    pip install oarepo-invenio-model
```
Usage
-----
The library provides extensible Invenio base record model.

JSON Schema
-----------
Add this package to your dependencies and use it via $ref in json
schema.

### Usage example
```json
{
  "type": "object",
  "allOf": [
    {
      "properties": {
        "title": {
          "type": "string"
        }
      }
    },
    {
      "$ref": "/schemas/invenio-v1.0.0.json#/definitions/InvenioRecord"
    }
  ],
  "additionalProperties": "false"
}
```
Elastic Search Mapping
----------------------
Use `oarepo-mapping-includes` library for extanding invenio base record model mapping.
### Usage example
```json
{
  "mappings": {
    "dynamic": "strict",
    "oarepo:extends": "invenio-v1.0.0.json#/InvenioRecord",
    "properties": {
         "title": {
        "type": "text"
      }
    }
  }
}
```

Marshmallow
-----------
You can extense your schema with Invenio base model schema by inheriting from `InvenioRecordMetadataSchemaV1Mixin`.

### Usage example
```python
class SampleSchemaV1(InvenioRecordMetadataSchemaV1Mixin):
    title = fields.String(validate=validate.Length(min=5), required=True)
```

Schema inheritance
------------------

JSON Schema provides ``allOf`` construct to join multiple schemas. The current
implementation of python's schema validator can not handle ``allOf`` in top-level
element.

To enable composition of schemas in the form of top-level "includes":

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "allOf": [
    {
      "$ref": "/schemas/dcterms-v2.0.0.json#/definitions/DCObject"
    },
    {
      "$ref": "/schemas/invenio-v1.0.0.json#/definitions/InvenioRecord"
    },
    {
      "properties": {
        "category": {
          "type": "string",
          "enum": ["kovy", "sklo", "keramika", "textil"]
        }
      }
    }
  ]
}
```
inherit your record class from ``InheritedSchemaRecordMixin``:

```python
from oarepo_invenio_model import InheritedSchemaRecordMixin
from invenio_records.api import Record

class MyRecord(InheritedSchemaRecordMixin, Record):
    pass
```



  [image]: https://img.shields.io/github/license/oarepo/oarepo-invenio-model.svg
  [1]: https://github.com/oarepo/oarepo-invenio-model/blob/master/LICENSE
  [2]: https://img.shields.io/travis/oarepo/oarepo-invenio-model.svg
  [3]: https://travis-ci.org/oarepo/oarepo-invenio-model
  [4]: https://img.shields.io/coveralls/oarepo/oarepo-invenio-model.svg
  [5]: https://coveralls.io/github/oarepo/oarepo-invenio-model
  [6]: https://img.shields.io/pypi/v/oarepo-invenio-model.svg
  [7]: https://pypi.org/pypi/oarepo-invenio-model