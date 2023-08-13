from pymaidol.AnnotationType import FULL_ANNOTATION_TYPE, AnnotationTypeEnum
from pymaidol.TemplateBase import TemplateBase

class SubClassTemplate(TemplateBase):
    def __init__(self, 
                 class_name:str, 
                 template: str | None = None, 
                 template_file_path: str | None = None, 
                 supported_annotation_types: list[AnnotationTypeEnum] = FULL_ANNOTATION_TYPE,
                 disable_annotation_types: list[AnnotationTypeEnum] = []) -> None:
        super().__init__(template, template_file_path, supported_annotation_types, disable_annotation_types)
        self.class_name = class_name
