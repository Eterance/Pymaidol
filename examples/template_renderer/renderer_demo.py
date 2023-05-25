import os
import sys
ROOT_DIR = os.path.join(os.path.dirname(__file__), "../../")
sys.path.append(ROOT_DIR)
from pymaidol import TemplateRenderer
from pymaidol.AnnotationType import SingleLineAnnotationTypeEnum

USELESS = "USELESS"

def main():
    renderer = TemplateRenderer.ReadFromFile("examples\\template_renderer\\template.pymd", [SingleLineAnnotationTypeEnum.C])
    alpha = 42
    beta = 3.14
    print(renderer.Render(
        {
            "global_vars": 
            {
                "USELESS": USELESS
            },
            "local_vars":
            {
                "alpha": alpha, 
                "beta": beta
            }
        }
    ))
    
if __name__ == "__main__":
    main()