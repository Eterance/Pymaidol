from typing import Optional
from pymaidol.AnnotationTypeEnum import AnnotationTypeEnum

class VisibleNode:
    pass

class InvisibleNode:
    pass

class HasBodyNode:
    def __init__(self) -> None:
        self.body:str = ""

class BaseNode: 
    def __init__(
        self,
        start_line:int, 
        start:int,
        total_start:int,
        father:Optional['NonTerminalNode'] = None,
        add_father_children:bool=False,
        *args,
        **kwargs) -> None:
        
        self.content = ""
        self.start_line = start_line 
        self.start:int = start # 从本行的第几个字符开始
        self.end_line = -1
        self.end:int = -1 # 从本行的第几个字符结束
        self.total_start:int = total_start # 从从头开始的第几个字符开始
        self.total_end:int = -1 # 从从头开始的第几个字符结束（包括这个字符，用在数组切片时要+1）
        self.father = father
        if self.father is not None and add_father_children:
            self.father.children.append(self)
        
    def __str__(self) -> str:
        return self.content
    
    def __repr__(self) -> str:
        return f'Start: {self.start_line}:{self.start}({self.total_start}), End: {self.end_line}:{self.end}({self.total_end}); {type(self)}, {[self.content]}'
    
    def append_content(self, string:str):
        self.content = f"{self.content}{string}"
    
    @classmethod
    def FromInstance(cls, baseNode:'BaseNode'):
        new_one = cls(baseNode.start_line, baseNode.start, baseNode.total_start)
        new_one.content = baseNode.content
        new_one.end_line = baseNode.end_line
        new_one.end = baseNode.end
        new_one.total_end = baseNode.total_end
        new_one.father = baseNode.father
        return new_one
    
class TerminalNode(BaseNode):
    pass
    
class NonTerminalNode(BaseNode, InvisibleNode, HasBodyNode):
    def __init__(
        self,
        *args,
        **kwargs) -> None: 
        super().__init__(*args, **kwargs)
        self.children:list[BaseNode] = []
        self.condition:Optional[str] = None    
    
    def append_content(self, string:str):
        self.content = f"{self.content}{string}"
    
    @classmethod
    def FromInstance(cls, baseNode:'BaseNode'):
        new_one = super().FromInstance(baseNode)
        if isinstance(baseNode, NonTerminalNode):
            new_one.children = baseNode.children
            new_one.condition = baseNode.condition
            new_one.body = baseNode.body
        return new_one

class TextNode(TerminalNode, VisibleNode):
    pass

class AnnotationNode(TerminalNode, InvisibleNode, HasBodyNode):
    def __init__(
        self,
        annotation_type:AnnotationTypeEnum,
        *args,
        **kwargs) -> None: 
        super().__init__(*args, **kwargs)
        self.type:AnnotationTypeEnum = annotation_type
    
    def __repr__(self) -> str:
        return f'Start: {self.start_line}:{self.start}({self.total_start}), End: {self.end_line}:{self.end}({self.total_end}); {self.type}, {[self.content]}'

# content 是不包括圆括号的表达式
class ShowBlockNode(TerminalNode, VisibleNode, HasBodyNode):
    pass

# content 是不包括花括号的python代码体
class CodeBlockNode(TerminalNode, InvisibleNode, HasBodyNode):
    pass

class IfNode(NonTerminalNode):
    pass

class ElifNode(NonTerminalNode):
    pass

# self.condition 无意义
class ElseNode(NonTerminalNode):
    pass

class ForNode(NonTerminalNode):
    pass

class WhileNode(NonTerminalNode):
    pass

class BreakNode(TerminalNode, InvisibleNode):
    pass

class ContinueNode(TerminalNode, InvisibleNode):
    pass

class EmptyNode(NonTerminalNode):
    pass