from typing import Optional
from pymaidol.AnnotationTypeEnum import AnnotationTypeEnum
from pymaidol.Positions import Position

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
        start_position:Position,
        father:Optional['NonTerminalNode'] = None,
        add_father_children:bool=False,
        *args,
        **kwargs) -> None:
        
        self.content = ""
        self.start_position:Position = start_position        
        self.end_position:Position = Position.Default()
        self.father = father
        if self.father is not None and add_father_children:
            self.father.children.append(self)
        
    def __str__(self) -> str:
        return self.content
    
    @property
    def PositionString(self):
        return f"Start: {self.start_position}, End: {self.end_position}"
    
    def __repr__(self) -> str:
        return f'{self.PositionString}; {type(self)}, {[self.content]}'
    
    def append_content(self, string:str):
        self.content = f"{self.content}{string}"
    
    @classmethod
    def FromInstance(cls, baseNode:'BaseNode'):
        new_one = cls(baseNode.start_position)
        new_one.content = baseNode.content
        new_one.end_position = baseNode.end_position
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
        return f'{self.PositionString}; {self.type}, {[self.content]}'

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