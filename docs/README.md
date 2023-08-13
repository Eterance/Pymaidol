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

## 第一个 Pymaidol 模板

### 创建模板文件

首先，假设你创建了一个名为 `pymaidol_test` 的文件夹。使用编辑器或者 IDE 打开该文件夹作为工作目录。

在 `pymaidol_test` 文件夹下打开命令行，输入以下命令：

``` bash
python -m pymaidol -n FirstTemplate
```

`FirstTemplate` 是模板类的类名。命令行会输出以下内容，同时文件夹中会生成 `FirstTemplate.pymd` 和 `FirstTemplate.py` 两个文件：

``` bash
Success: file "FirstTemplate.pymd" created
Success: file "FirstTemplate.py" created
```

### 编写模板设计文件

首先，用以下代码将 `FirstTemplate.pymd` 中的全部内容替换掉：

``` python
from pymaidol import TemplateBase
from pymaidol.AnnotationType import FULL_ANNOTATION_TYPE, AnnotationTypeEnum

class FirstTemplate(TemplateBase):
    def __init__(self, 
                 package_name:str, 
                 template: str | None = None, 
                 template_file_path: str | None = None, 
                 supported_annotation_types: list[AnnotationTypeEnum] = FULL_ANNOTATION_TYPE,
                 disable_annotation_types: list[AnnotationTypeEnum] = []) -> None:
        super().__init__(template, template_file_path, supported_annotation_types, disable_annotation_types)
        self.package_name = package_name
        
def main():
    template = FirstTemplate("Pymaidol")
    string = template.Render({"says": "Hello World"})
    print(string)
    
if __name__ == "__main__":
    main()
```

这段代码主要修改了以下部分：

- 为 `FirstTemplate` 类添加了 `package_name` 属性。
- 添加了 `main` 函数，以实例化 `FirstTemplate` 类。向 `FirstTemplate` 类的构造函数传入了 `package_name` 参数，该参数的值为 `Pymaidol`。
- 调用了 `Render` 方法，向其传入了一个字典 `{"says": "Hello World"}`。

然后，用以下代码替换 `FirstTemplate` 类中的全部内容：

``` python
@{import time}
Now (@(time.ctime())), Say "@(says)" using @(self.package_name)!
```

运行 `FirstTemplate.py`，命令行会输出以下内容：

``` bash
Now (Tue May 23 19:21:19 2023), Say "Hello World" using Pymaidol!
```

## 另请参阅

- [Pymaidol 语法参考](zh-cn/语法参考.md)
- [Pymaidol API 目录](zh-cn/Pymaidol_API目录.md)
