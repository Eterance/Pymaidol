# Position 类

## 概述

`Position` 类用于定位在原始模板字符串中的位置。

`Position` 的对象里的属性是只读的，初始化之后不允许被修改。

注意：当 `Position` 类用于结束位置时，是包括该位置的字符的。比如：如果 `start.total = 20`， `end.total = 30`，那么对原模板字符串的切片应该为 `template[20:31]`。

模块：pymaidol.Positions

## 导入

```python
from pymaidol import Position
```

或

```python
from pymaidol.Positions import Position
```

## 构造函数

### `Position(line_index, char_index, total)`

#### 参数

- `line_index` (int): 行索引。从 0 开始。
- `char_index` (int): 当前行的字符索引。从 0 开始。
- `total` (int): 字符索引。从 0 开始。

## 属性

### `line_index` (int，readonly)

行索引。从 0 开始。

### `char_index` (int，readonly)

当前行的字符索引。从 0 开始。

### `total` (int，readonly)

字符索引。从 0 开始。

### `full_description` (str，readonly)

完整的、人类可读的位置描述。

## 方法

### `Position.Default()`

@ classmethod

新建并返回一个默认的 `Position` 对象，其所有属性均为 0。

#### 参数

无。

#### 返回值 (`Position`)

默认的 `Position` 对象。

### `Copy()`

复制并返回一个新的 `Position` 对象。

#### 参数

无。

#### 返回值 (`Position`)

新的 `Position` 对象，且其所有属性与原对象相同。
