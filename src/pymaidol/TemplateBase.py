
import os
from typing import Optional
from pymaidol.Part import Parser


class TemplateBase:
    def __init__(self, template:Optional[str]=None, template_file_path:Optional[str]=None) -> None:  
        self._template:Optional[str] = template
        if self._template == None:
            self._template = self._ReadTemplate(template_file_path)
        pr = Parser()
        self._node = pr.Parse(self._template)
    
    def _ReadTemplate(self, template_file_path:Optional[str]=None)->str:
        if template_file_path is None:
            template_file_path =__file__[:-3] + ".pml"
        try: 
            with open(template_file_path, "r", encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError as fex:
            fex.strerror = f"No such template design file"
            raise fex
    
    def Render(self, **inject_kwargs):
        raise NotImplementedError()
    
    def TranslateToPython(self):
        raise NotImplementedError()
