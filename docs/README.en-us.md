# Pymaidol

[简体中文](README.md) | English

**All English docs are translated by Chat-GPT. Feel free to submit a PR to improve the translation.**

Pymaidol is a markup syntax for embedding Python code into text, allowing the content to be dynamically changed at runtime.

Compared to [ProMaid](https://github.com/Eterance/ProMaid), Pymaidol not only embeds data into corresponding positions in templates, but also allows complex processing logic to be presented in templates. It can even use functions defined in templates to process data.

⚠ **Warning: Pymaidol is currently in the development stage, and the syntax and some handling logic for whitespace and line breaks are not yet finalized and may be subject to change in the future. It is strongly recommended not to use it in a production environment.**

## Requirements and Installation

python >= 3.10

``` bash
pip install Pymaidol -i https://pypi.python.org/simple
```

## The First Pymaidol Template

### Creating a Template File

First, assume you have created a folder named `pymaidol_test`. Open the folder as the working directory using an editor or IDE.

Open the command line in the `pymaidol_test` folder and enter the following command:

``` bash
python -m pymaidol -n FirstTemplate
```

`FirstTemplate` is the class name of the template. The command line will output the following content, and two files, `FirstTemplate.pymd` and `FirstTemplate.py`, will be generated in the folder:

``` bash
Success: file "FirstTemplate.pymd" created
Success: file "FirstTemplate.py" created
```

### Writing the Template Design File

First, replace all the contents in `FirstTemplate.pymd` with the following code:

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

This code mainly modifies the following parts:

- Adds the `package_name` attribute to the `FirstTemplate` class.
- Adds the `main` function to instantiate the `FirstTemplate` class. The `package_name` parameter is passed to the constructor of the `FirstTemplate` class with a value of `Pymaidol`.
- Calls the `Render` method and passes a dictionary `{"says": "Hello World"}` to it.

Then, replace all the contents in the `FirstTemplate` class with the following code:

``` python
@{import time}
Now (@(time.ctime())), Say "@(says)" using @(self.package_name)!
```

Run `FirstTemplate.py`, and the command line will output the following content:

``` bash
Now (Tue May 23 19:21:19 2023), Say "Hello World" using Pymaidol!
```

## See Also

- [Pymaidol Syntax Reference](en-us/Syntax_Reference.md)
- [Pymaidol API Directory](en-us/Pymaidol_API_Directory.md)
