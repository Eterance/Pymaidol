from pymaidol.TemplateBase import TemplateBase

class test_class(TemplateBase):
    def __init__(self, template: str | None = None, template_file_path: str | None = None) -> None:
        super().__init__(template, template_file_path)