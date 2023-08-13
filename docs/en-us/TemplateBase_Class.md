# TemplateBase Class

## Overview

The `TemplateBase` class is the backend class for Pymaidol templates and serves as the base class for all Pymaidol template classes. It is an abstract class that cannot be instantiated and needs to be inherited for use.

Module: pymaidol.TemplateBase

Inherits from: abc.ABC

## Import

```python
from pymaidol import TemplateBase
```

or

```python
from pymaidol.TemplateBase import TemplateBase
```

## Constructor

### `TemplateBase(template, template_file_path, supported_annotation_types, disable_annotation_types)` (virtual)

#### Parameters

- `template` (str, optional): The template string. Default is `None`.
- `template_file_path` (str, optional): The template file path. Default is `None`.
- `supported_annotation_types` (list[AnnotationTypeEnum], optional): The list of supported annotation types. Default is all annotation types (Python, C single-line and multi-line comments, HTML comments).
- `disable_annotation_types` (list[AnnotationTypeEnum], optional): The list of disabled annotation types, making these annotations appear in the rendered text. Default is empty. Disabled annotations take precedence over supported annotations. For example, if `AnnotationTypeEnum.SingleLineAnnotationTypeEnum.Python` (Python single-line comments) is included in `disable_annotation_types`, it will be disabled regardless of whether it is included in `supported_annotation_types`.

When both `template` and `template_file_path` are `None`, the `TemplateBase` class and its subclasses will attempt to read the template file `.pymd` with the same name in the same directory as itself. If both are not empty, `template` will be used as a priority.

## Attributes

### `rendered` (str, readonly)

The rendered string. If `Render()` method has not been called since self-initialization or calling `HotReload()` method, it will be `None`.

### `template` (str, readonly)

The template string.

## Methods

### `HotReload(template, template_file_path)` (final)

Reloads the template.

#### Parameters

- `template` (str, optional): The template string. Default is `None`.
- `template_file_path` (str, optional): The template file path. Default is `None`.

When both `template` and `template_file_path` are `None`, the `TemplateBase` class and its subclasses will attempt to read the template file `.pymd` with the same name in the same directory as itself. If both are not empty, `template` will be used as a priority.

#### Returns (`None`)

None.


### `Render(inject_kwargs)` (final)

Renders the template string with the given data.

#### Parameters

- `inject_kwargs` (dict, Optional): The externally injected variables used for rendering the template string. Default is `None`. The injected variables will be treated as local variables.

#### Returns (`str`)

The rendered string.
