from TemplateBase import TemplateBase

class SubClassTemplate(TemplateBase):
    def __init__(self, class_name:str, template: str | None = None, template_file_path: str | None = None) -> None:
        super().__init__(template, template_file_path)
        self.class_name = class_name
