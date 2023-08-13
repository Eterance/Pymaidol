# MultiLineAnnotationTypeEnum Enum

## Overview

Contains the types of multiline annotations that can be used in template design files `.pymd`.

Module: [pymaidol.AnnotationType](AnnotationType_Module.md)

Inherits from: [pymaidol.AnnotationType.AnnotationTypeEnum](AnnotationTypeEnum_Enumeration.md)

## Import

```python
from pymaidol import MultiLineAnnotationTypeEnum
```

or

```python
from pymaidol.AnnotationType import MultiLineAnnotationTypeEnum
```

## Enum Items

Name | Value | Description
--- | --- | ---
Python | ''' | Multiline comment in Python, which starts and ends with `'''`.
C | /\* | Multiline comment in C, which starts with `/\*` and ends with `*/`.
HTML | \<!-- | Multiline comment in HTML, which starts with `<!--` and ends with `-->`.