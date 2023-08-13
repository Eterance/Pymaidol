# Position Class

## Overview

The `Position` class is used to locate positions in the original template string.

The properties of the `Position` object are read-only and cannot be modified after initialization.

Note: When the `Position` class is used for the end position, it includes the character at that position. For example, if `start.total = 20` and `end.total = 30`, the slice of the original template string should be `template[20:31]`.

Module: pymaidol.Positions

## Import

```python
from pymaidol import Position
```

or

```python
from pymaidol.Positions import Position
```

## Constructor

### `Position(line_index, char_index, total)`

#### Parameters

- `line_index` (int): Line index. Starting from 0.
- `char_index` (int): Character index of the current line. Starting from 0.
- `total` (int): Total character index. Starting from 0.

## Properties

### `line_index` (int, readonly)

Line index. Starting from 0.

### `char_index` (int, readonly)

Character index of the current line. Starting from 0.

### `total` (int, readonly)

Total character index. Starting from 0.

### `full_description` (str, readonly)

Complete and human-readable position description.

## Methods

### `Position.Default()`

@ classmethod

Create and return a default `Position` object with all properties set to 0.

#### Parameters

None.

#### Returns (`Position`)

Default `Position` object.

### `Copy()`

Copy and return a new `Position` object.

#### Parameters

None.

#### Returns (`Position`)

New `Position` object with the same properties as the original object.
