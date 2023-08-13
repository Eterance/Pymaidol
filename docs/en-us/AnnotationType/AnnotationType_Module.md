# AnnotationType Module

## Overview

The `AnnotationType` module provides an enumeration of annotations that can be used in template design files with the `.pymd` extension.

Module: `pymaidol`

## Import

```python
from pymaidol import AnnotationType
```

## Classes

Name | Description
--- | ---
[AnnotationTypeEnum Enumeration](AnnotationTypeEnum_Enumeration.md) | The `AnnotationTypeEnum` enumeration is the base class for all annotation type enumerations. It does not contain any enumeration values and is only used for inheritance.
[SingleLineAnnotationTypeEnum Enumeration](SingleLineAnnotationTypeEnum_Enumeration.md) | Contains the types of single-line annotations that can be used in template design files with the `.pymd` extension.
[MultiLineAnnotationTypeEnum Enumeration](MultiLineAnnotationTypeEnum_Enumeration.md) | Contains the types of multi-line annotations that can be used in template design files with the `.pymd` extension.

## Static Variables

Name | Type | Description
--- | --- | ---
FULL_ANNOTATION_TYPE | `list[AnnotationTypeEnum]` | A list that contains all the enumeration values of the annotation type enumerations.
