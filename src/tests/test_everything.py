import json
import os
import random
import sys
from tqdm import tqdm


ROOT_DIR = os.path.join(os.path.dirname(__file__), "../../")
SRC_DIR = os.path.join(ROOT_DIR, "src")
sys.path.append(ROOT_DIR)
sys.path.append(SRC_DIR)
from pymaidol.TemplateBase import TemplateBase
from pymaidol.AnnotationTypeEnum import MultiLineAnnotationTypeEnum
from tests.harder_demo.CodeLangTemplate import CodeLangTemplate

gol = 23
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
        
    def exec(self):
        alfa = 1
        liker = "sasas"
        gol = 2234234
        print(gol)
    

def main():
    with open(r"F:\Programs3\Deep_Learning_Repo\pymaidol\src\tests\harder_demo\codelang.json", "r", encoding='utf-8') as f: 
        data = json.load(f)
    sasas = CodeLangTemplate()
    kwargs = {"incontext_samples": data[0:3], "query_sample": data[3]}
    prompt = sasas.Render(kwargs)
    print(prompt)
    
if __name__ == "__main__":
    main()