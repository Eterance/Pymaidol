# MultiLineAnnotationTypeEnum 枚举

## 概述

包含了可在模板设计文件中`.pymd`使用的多行注释的类型。

模块：[pymaidol.AnnotationType](AnnotationType模块.md)

继承自：[pymaidol.AnnotationType.AnnotationTypeEnum](AnnotationTypeEnum枚举.md)

## 导入

```python
from pymaidol import MultiLineAnnotationTypeEnum
```

或

```python
from pymaidol.AnnotationType import MultiLineAnnotationTypeEnum
```

## 枚举项

名称 | 值 | 描述
--- | --- | ---
Python | ''' | Python 的多行注释，即以 `'''` 开头和结尾的注释。
C | /\* | C 的多行注释，即以 `/\*` 开头和 `*/` 结尾的注释。
HTML | \<!-- | HTML 的多行注释，即以 `<!--` 开头和 `-->` 结尾的注释。
