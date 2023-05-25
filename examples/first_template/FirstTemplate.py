from pymaidol import TemplateBase
from pymaidol.AnnotationType import FULL_ANNOTATION_TYPE, AnnotationTypeEnum

class FirstTemplate(TemplateBase):
    def __init__(self, 
                 package_name:str, 
                 template: str | None = None, 
                 template_file_path: str | None = None, 
                 supported_annotation_types: list[AnnotationTypeEnum] = FULL_ANNOTATION_TYPE) -> None:
        super().__init__(template, template_file_path, supported_annotation_types)
        self.package_name = package_name
        
def main():
    template = FirstTemplate("Pymaidol")
    string = template.Render({"says": "Hello World"})
    print(string)
    
if __name__ == "__main__":
    main()