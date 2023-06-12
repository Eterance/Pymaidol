
from collections.abc import Iterable
from enum import Enum
from typing import Any

from pymaidol.Errors import (LackingConditionError, NameException, PythonExecutionError,
                    TypeException, WrongForStatement)
from pymaidol.Nodes import (AnnotationNode, BaseNode, BodyComponent, BranchRole,
                   BreakNode, CodeBlockNode, ComponentOrRole, ContinueNode,
                   ElifNode, ElseNode, EmptyNode, ForNode, IfNode,
                   InvisibleRole, LoopRole, NonTerminalNode, ShowBlockNode,
                   TerminalNode, TextNode, VisibleRole, WhileNode)


class ControlResultEnum(Enum):
    Default = "Default"
    Break = "Break"
    Continue = "Continue"


class Executor:
    def __init__(self, root:BaseNode) -> None:
        self._root = root
        self._prompt = ""
    
    @property
    def root(self):
        return self._root
        
    def Execute(self, global_var:dict[str, Any], local_var:dict[str, Any]) -> str:
        self._prompt = ""
        self._recursive_traverse(self._root, global_var, local_var)
        return self._prompt
        
    def _recursive_traverse(self, node:BaseNode, global_var:dict[str, Any], local_var:dict[str, Any]) -> ControlResultEnum:
        if isinstance(node, NonTerminalNode):
            if isinstance(node, (IfNode, ElifNode)):
                try:
                    result = eval(node.condition, global_var, local_var)
                    if result:
                        for child in node.children:
                            result = self._recursive_traverse(child, global_var, local_var)
                            if result == ControlResultEnum.Break or result == ControlResultEnum.Continue:
                                return result
                        return ControlResultEnum.Default
                    else:
                        if node.next_branch is not None:
                            return self._recursive_traverse(node.next_branch, global_var, local_var)
                        else:
                            return ControlResultEnum.Default
                except Exception as ex:
                    raise PythonExecutionError(node.start, ex)
            
            elif isinstance(node, ElseNode):
                for child in node.children:
                    result = self._recursive_traverse(child, global_var, local_var)
                    if result == ControlResultEnum.Break or result == ControlResultEnum.Continue:
                        return result
                return ControlResultEnum.Default
                
            elif isinstance(node, ForNode):
                # 提取变量名和可枚举对象
                strings = node.condition.split(" in ")
                assert len(strings) == 2, WrongForStatement(node.start)
                variables_string = strings[0].strip()
                try:
                    enumerate_object = eval(strings[1].strip(), global_var, local_var)
                except NameError as ne:
                    raise NameException(node.start, str(ne))
                assert isinstance(enumerate_object, Iterable), TypeException(node.start, f"{strings[1].strip()} ({type(enumerate_object)}) is not iterable")
                
                try:
                    for element in enumerate_object:
                        exec(f"{variables_string} = {element}", global_var, local_var)
                        for child in node.children:
                            result = self._recursive_traverse(child, global_var, local_var)
                            if result == ControlResultEnum.Break:
                                return ControlResultEnum.Default
                            elif result == ControlResultEnum.Continue:
                                break
                    return ControlResultEnum.Default
                except Exception as ex:
                    raise PythonExecutionError(node.start, ex)
                
            elif isinstance(node, WhileNode):
                try:
                    while (result := eval(node.condition, global_var, local_var)):
                        for child in node.children:
                            result = self._recursive_traverse(child, global_var, local_var)
                            if result == ControlResultEnum.Break:
                                return ControlResultEnum.Default
                            elif result == ControlResultEnum.Continue:
                                break
                    return ControlResultEnum.Default
                except Exception as ex:
                    raise PythonExecutionError(node.start, ex)
            
            else:
                for child in node.children:
                    self._recursive_traverse(child, global_var, local_var)
                return ControlResultEnum.Default
        else:
            if type(node) == TextNode:
                self._prompt = f"{self._prompt}{node.content}"
                
            elif type(node) == ShowBlockNode:
                try:
                    self._prompt = f"{self._prompt}{eval(node.body, global_var, local_var)}"
                except Exception as ex:
                    raise PythonExecutionError(node.start, ex)
                
            elif type(node) == CodeBlockNode:
                try:
                    exec(node.body, global_var, local_var)
                except Exception as ex:
                    raise PythonExecutionError(node.start, ex)
                
            elif type(node) == BreakNode:
                return ControlResultEnum.Break
            
            elif type(node) == ContinueNode:
                return ControlResultEnum.Continue
            
        return ControlResultEnum.Default