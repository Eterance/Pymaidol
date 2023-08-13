# TemplateRenderer Class

## Overview

A class that renders template strings into strings.

Module: pymaidol.TemplateRenderer

## Import

```python
from pymaidol import TemplateRenderer
```

or

```python
from pymaidol.TemplateRenderer import TemplateRenderer
```

## Constructor

### `TemplateRenderer(template, supported_annotation_types)`

#### Parameters

- `template` (str): The template string.
- `supported_annotation_types` (list[AnnotationTypeEnum], optional): The list of supported annotation types. Defaults to all annotation types (Python, C single-line and multi-line comments, HTML comments).

## Attributes

### `template` (str, readonly)

The template string.

## Methods

### `TemplateRenderer.ReadFromFile(template_file_path, supported_annotation_types)` (classmethod)

Given a template file path, returns a `TemplateRenderer` object.

#### Parameters

- `template_file_path` (str): The template file path.
- `supported_annotation_types` (list[AnnotationTypeEnum]): The list of supported annotation types.

#### Returns

`TemplateRenderer`: The `TemplateRenderer` object.

### `Render(local_vars, global_vars)` (final)

Renders the template string with the given data.

#### Parameters

- `local_vars` (dict): The local variables used for rendering the template string.
- `global_vars` (dict, optional): The global variables used for rendering the template string. Defaults to `None`.

#### Returns

`str`: The rendered string.
