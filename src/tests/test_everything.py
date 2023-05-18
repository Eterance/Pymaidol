import json
import os
import random
import sys


ROOT_DIR = os.path.join(os.path.dirname(__file__), "../../")
SRC_DIR = os.path.join(ROOT_DIR, "src")
sys.path.append(ROOT_DIR)
sys.path.append(SRC_DIR)
from pymaidol.TemplateBase import TemplateBase
from pymaidol.AnnotationTypeEnum import MultiLineAnnotationTypeEnum

class father:
    def __init__(self) -> None:
        self.a = 1
    
    @classmethod
    def from_exist(cls, obj:'father'):
        new_one = cls()
        new_one.a = obj.a
        return new_one
    
class son(father):
    def __init__(self) -> None:
        super().__init__()
        self.b = 2
    

def main():
    sss = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    sss = sss[:-1]
    sd =  23
    result = isinstance(MultiLineAnnotationTypeEnum.C, MultiLineAnnotationTypeEnum)
    sasas = TemplateBase(template_file_path=r"F:\Programs3\Deep_Learning_Repo\pymaidol\src\tests\harder_demo\CodeLangTemplate.pml")
    try:
        exec("print(self.incontext_samsples)", {}, {"self": sasas})
    except Exception as ex:
        print(ex)
    print("ok!")
    
if __name__ == "__main__":
    main()