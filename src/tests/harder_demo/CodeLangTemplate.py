
from typing import Optional
from pymaidol.TemplateBase import TemplateBase

class CodeLangTemplate(TemplateBase):
    def __init__(self, template: str | None = None, template_file_path: str | None = None) -> None:
        super().__init__(template, template_file_path)
