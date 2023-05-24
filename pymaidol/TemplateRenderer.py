
import inspect
from abc import ABC, abstractmethod
from typing import Any, Optional, final

from pymaidol.Executor import Executor
from pymaidol.Parser import Parser
from pymaidol.SyntaxChecker import SyntaxChecker

class TemplateRenderer():
    def __init__(self, template:str) -> None:
        self._template:str = template        
        self._node = Parser(self._template).Parse()
        self._node = SyntaxChecker().Check(self._node)
        self._executor = Executor(self._node)
        
    @classmethod
    def ReadFromFile(cls, template_file_path:str)->"TemplateRenderer":
        try: 
            with open(template_file_path, "r", encoding='utf-8') as f:
                return cls(f.read())
        except FileNotFoundError as fex:
            fex.strerror = f"No such template design file"
            raise fex
    
    @property
    def template(self):
        return self._template
        
    @final
    def Render(self, global_vars:dict, local_vars:dict) -> str:
        return self._executor.Execute(global_vars, local_vars)
    
    @final
    def TranslateToPython(self) -> str:
        raise NotImplementedError()