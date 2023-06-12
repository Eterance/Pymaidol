import json
import os
import random
import sys
from tqdm import tqdm



ROOT_DIR = os.path.join(os.path.dirname(__file__), "../../")
SRC_DIR = os.path.join(ROOT_DIR, "src")
sys.path.append(ROOT_DIR)
sys.path.append(SRC_DIR)
from tests.din.ContextDebugTemplate import ContextDebugTemplate
from pymaidol import SingleLineAnnotationTypeEnum

cdt = ContextDebugTemplate(disable_annotation_types=[SingleLineAnnotationTypeEnum.Python, SingleLineAnnotationTypeEnum.C])

for index in range(10):
    cdt.fields = f"hello!{index}"
    cdt.nl = "nl"
    cdt.sql = "predict"
    cdt.error = "error"
    prompt = cdt.Render()
    print(prompt)
    print(f"-------------------- 分割线 ---------------------")