
import inspect
from abc import ABC, abstractmethod
from typing import Any, Optional, final

from pymaidol.Executor import Executor
from pymaidol.Parser import Parser
from pymaidol.SyntaxChecker import SyntaxChecker


class TemplateBase(ABC):
    @abstractmethod
    def __init__(self, template:Optional[str]=None, template_file_path:Optional[str]=None) -> None:  
        self._template:str = ""
        self._template_file_path:Optional[str] = template_file_path
        self.HotReload(template, template_file_path)
        self._rendered:Optional[str] = None
    
    @property
    def template(self): 
        return self._template
    
    @property
    def rendered(self): 
        '''
        模板设计文件渲染后的结果。如果初始化或热重载以来没有渲染过，则为None。
        '''
        return self._rendered    
    
    @final
    def HotReload(self, template:Optional[str]=None, template_file_path:Optional[str]=None):
        """ 热重载模板设计文件。如果不指定模板设计文件路径，则使用初始化时指定的模板设计文件路径或者检测到的模板设计文件路径。

        Args:
            template_file_path (Optional[str], optional): 模板设计文件路径. Defaults to None.
        """
        if template is not None:
            self._template = template
        elif template_file_path is not None:
            self._template_file_path = template_file_path
            self._template = self._ReadTemplate(self._template_file_path)
        else:
            # 获取类的文件路径
            # https://stackoverflow.com/a/697395
            self._template_file_path = inspect.getfile(self.__class__)[:-3] + ".pymd"
            self._template = self._ReadTemplate(self._template_file_path)
        self._rendered = None
        self._node = Parser(self._template).Parse()
        self._node = SyntaxChecker().Check(self._node)
        self._executor = Executor(self._node)
    
    @final
    def _ReadTemplate(self, template_file_path)->str:
        try: 
            with open(template_file_path, "r", encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError as fex:
            fex.strerror = f"No such template design file"
            raise fex
    
    @final
    def Render(self, inject_kwargs:Optional[dict[str, Any]] = None) -> str:
        global_vars:dict[str, Any] = {}
        local_vars = {"self": self}
        if inject_kwargs is not None:
            global_vars.update(inject_kwargs)
        result = self._executor.Execute(global_vars, local_vars)
        self._rendered = result
        return result
    
    @final
    def TranslateToPython(self) -> str:
        raise NotImplementedError()
