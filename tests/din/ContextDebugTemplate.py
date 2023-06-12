from pymaidol.AnnotationType import FULL_ANNOTATION_TYPE, AnnotationTypeEnum
from pymaidol.TemplateBase import TemplateBase

class ContextDebugTemplate(TemplateBase):
    def __init__(self,
                 template: str | None = None,
                 template_file_path: str | None = None,
                 supported_annotation_types: list[AnnotationTypeEnum] = FULL_ANNOTATION_TYPE,
                 disable_annotation_types:'list[AnnotationTypeEnum]' = []) -> None:
        super().__init__(template, template_file_path, supported_annotation_types, disable_annotation_types)
        self.fields:str = ""
        self.nl = ""
        self.sql = ""
        self.error = ""