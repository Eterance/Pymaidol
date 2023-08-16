# Pymaidol

简体中文 | [English](README.en-us.md)

Pymaidol 是一种标记语法，用于将 Python 代码嵌入文本中，使得文本在运行时可动态更改包含的内容。

与 [ProMaid](https://github.com/Eterance/ProMaid) 相比，Pymaidol 不只是单纯的将数据嵌入至模板（Template）的对应位置，还能将复杂的处理逻辑呈现在模板中，甚至可使用在模板中定义的函数对数据进行处理。

⚠**警告：Pymaidol 目前处于开发阶段，语法和一些对空白符、换行符的处理逻辑尚未确定，以后可能会被修改。强烈不建议在生产环境中使用。**

## 环境要求与安装

python >= 3.10

``` bash
pip install Pymaidol -i https://pypi.python.org/simple
```

## 文档

参见： https://eterance.github.io/Pymaidol-Docs/