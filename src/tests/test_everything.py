import json
import os
import random
import sys


ROOT_DIR = os.path.join(os.path.dirname(__file__), "../../")
SRC_DIR = os.path.join(ROOT_DIR, "src")
sys.path.append(ROOT_DIR)
sys.path.append(SRC_DIR)
from pymaidol.TemplateBase import TemplateBase

def main():
    asas = eval("[i*2 for i in range(10)]")
    aas:str = ""
    print(aas.startswith("asas"))
    sasas = TemplateBase(template_file_path=r"F:\Programs3\Deep_Learning_Repo\pymaidol\src\tests\harder_demo\CodeLangTemplate.pml")
    try:
        exec("print(self.incontext_samsples)", {}, {"self": sasas})
    except Exception as ex:
        print(ex)
    print("ok!")
    
if __name__ == "__main__":
    main()