
from typing import Optional
from pymaidol.TemplateBase import TemplateBase

class CodeLangTemplate(TemplateBase):
    def __init__(self, incontext_samples, query_sample, template: str | None = None, template_file_path: str | None = None,) -> None:
        super().__init__(template, template_file_path)
        self.incontext_samples = incontext_samples
        self.query_sample = query_sample
