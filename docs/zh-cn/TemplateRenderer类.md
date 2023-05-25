# TemplateRenderer 类

## 概述

将模板字符串渲染为字符串的类。

模块：pymaidol.TemplateRenderer

## 导入

```python
from pymaidol import TemplateRenderer
```

或

```python
from pymaidol.TemplateRenderer import TemplateRenderer
```

## 构造函数

### `TemplateRenderer(template, supported_annotation_types)`

#### 参数

- `template` (str): 模板字符串。
- `supported_annotation_types` (list[AnnotationTypeEnum], optional): 支持的注释类型列表。默认为所有注释类型（Python、C的单行与多行注释、HTML注释）。

## 属性

### `template`（str，readonly）

模板字符串。

## 方法

### `TemplateRenderer.ReadFromFile(template_file_path, supported_annotation_types)` (classmethod)

给定模板文件路径，返回一个 `TemplateRenderer` 对象。

#### 参数

- `template_file_path` (str): 模板文件路径。
- `supported_annotation_types` (list[AnnotationTypeEnum]): 支持的注释类型列表。

#### 返回值 

`TemplateRenderer`: `TemplateRenderer` 对象。

### `Render(local_vars, global_vars)` (final)

给与数据并渲染模板字符串。

#### 参数

- `local_vars` (dict): 用于渲染模板字符串的局部变量。
- `global_vars` (dict，可选): 用于渲染模板字符串的全局变量。默认为 `None`。

#### 返回值 

`str`: 渲染后的字符串。