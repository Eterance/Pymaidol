# AnnotationType 模块

## 概述

`AnnotationType` 模块提供了可在模板设计文件中`.pymd`使用的注释的枚举类型。

模块：`pymaidol`

## 导入

```python
from pymaidol import AnnotationType
```

## 类

名称 | 描述
--- | ---
[AnnotationTypeEnum 枚举](AnnotationTypeEnum枚举.md) | `AnnotationTypeEnum` 枚举是所有注释种类枚举类的基类。内部无枚举值，只用于被继承。
[SingleLineAnnotationTypeEnum 枚举](SingleLineAnnotationTypeEnum枚举.md) | 包含了可在模板设计文件中`.pymd`使用的单行注释的类型。
[MultiLineAnnotationTypeEnum 枚举](MultiLineAnnotationTypeEnum枚举.md) | 包含了可在模板设计文件中`.pymd`使用的多行注释的类型。

## 静态变量

名称 | 类型 | 描述
--- | --- | ---
FULL_ANNOTATION_TYPE | `list[AnnotationTypeEnum]` | 包含了所有注释种类枚举类的枚举值的列表。
