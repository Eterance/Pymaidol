# Pymaidol Syntax Reference

## Creating and Structure of Pymaidol Template Files

### Creating Template Files Using Command Line (Recommended)

Use the following command to create a template file:

``` bash
python -m pymaidol -n <class_name> [-d <directory>]
```

This will generate two files, `<class_name>.pymd` and `<class_name>.py`, in the current directory.

### Composition of Pymaidol Template Files

A template file consists of a template design file `.pymd` and a template backend file `.py`.

Template design file `.pymd`: Contains the design content of the template, such as strings and Python code/render expressions embedded with Pymaidol syntax.

Template backend file `.py`: Contains the backend logic of the template, such as the definition of the template class.

Variables and methods defined in the backend file can be accessed in the design file, but elements defined in the design file cannot be accessed in the backend file. In addition, the `import` statements in both files are independent.

> If manually creating Pymaidol template files, the file names of the template design file `.pymd` and the template backend file `.py` must be the same and located in the same folder. The file name of the template backend file must be the same as the class name of the template.

## Pymaidol Syntax

Pymaidol uses `@` as a marker to indicate Pymaidol expressions, keywords, and code blocks. To use `@` in text, please use `@@` instead.

## Pymaidol Expressions

Pymaidol expressions are used to embed/render data into the template. The format of a Pymaidol expression is `@(<expression>)`, for example:

``` python
@("Hello World!")
```

The rendered text is:

``` python
Hello World!
```

### Pymaidol Keywords

The format of keywords is `@<keyword>;`, for example:

``` python
@break; # Exit the current loop
@continue; # Skip the current iteration
```

### Pymaidol Code Blocks

Pymaidol code blocks are used to execute Python code during template rendering. The format is `@{<code_block>}`, for example:

``` python
@{answer = 42}
The answer of this universe is @(answer)
```

The rendered text is:

``` python
The answer of this universe is 42
```

Because rendering Pymaidol code blocks is done in the order from top to bottom and from left to right, you can use Pymaidol code blocks to define variables, functions, etc., and use them in subsequent expressions or code blocks.

### if, elif, else Code Blocks

The usage is `@if (<conditional_expression>){<template_design_statement>}`, for example:

``` python
@{answer = 42}
@if (answer > 0) {answer == @(answer), and it is positive.}
@elif (answer < 0) {answer == @(answer), and it is negative.}
@else {answer == @(answer), and it is zero.}
```

The rendered text is:

``` python
answer == 42, and it is positive.
```

### while Code Blocks

The usage is `@while (<conditional_expression>){<template_design_statement>}`, for example:

``` python
@{i = 0}
@while (i < 5){
i = @(i)
@{i += 1}
}
```

The rendered text is:

``` python
i = 0
i = 1
i = 2
i = 3
i = 4
```

### for Code Blocks

The usage is `@for (<variable> in <iterable_object>){<template_design_statement>}`, for example:

``` python
@for (i in range(5)){
i = @(i)
@if (i == 3) {@break;}
}
```

The rendered text is:

``` python
i = 0
i = 1
i = 2
i = 3
```
