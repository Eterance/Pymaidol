from typing import Optional
from pymaidol.AnnotationTypeEnum import AnnotationTypeEnum
from pymaidol.Positions import Position
from abc import ABC

class ComponentOrRole(ABC):
    '''
    通过继承该类，实现的抽象子类可以用作其他结点类的组件类被继承。\n
    可以往实例结点中添加成员变量，或者赋予实例结点某种身份。
    '''
    pass

class VisibleRole(ComponentOrRole, ABC):
    pass

class InvisibleRole(ComponentOrRole, ABC):
    pass

class BodyComponent(ComponentOrRole, ABC):
    def __init__(self) -> None:
        self.body:str = ""
        

class BranchRole(ComponentOrRole, ABC):
    def __init__(self) -> None: 
        self.previous_branch:Optional[BranchRole] = None
        self.next_branch:Optional[BranchRole] = None
        
class LoopRole(ComponentOrRole, ABC):
    pass

class BaseNode(ABC): 
    def __init__(
        self,
        start_position:Position,
        father:Optional['NonTerminalNode'] = None,
        add_father_children:bool=False,
        *args,
        **kwargs) -> None:
        
        self.content = ""
        self.start:Position = start_position        
        self.end:Position = Position.Default()
        self.father = father
        if self.father is not None and add_father_children:
            self.father.children.append(self)
        
    def __str__(self) -> str:
        return self.content
    
    @property
    def PositionString(self):
        return f"Start: {self.start}, End: {self.end}"
    
    def __repr__(self) -> str:
        return f'{self.PositionString}; {type(self)}, {[self.content]}'
    
    def append_content(self, string:str):
        self.content = f"{self.content}{string}"
    
    @classmethod
    def FromInstance(cls, baseNode:'BaseNode'):
        new_one = cls(baseNode.start)
        new_one.content = baseNode.content
        new_one.end = baseNode.end
        new_one.father = baseNode.father
        return new_one
    
class TerminalNode(BaseNode, ABC):
    pass
    
class NonTerminalNode(BaseNode, InvisibleRole, BodyComponent, ABC):
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

class TextNode(TerminalNode, VisibleRole):
    pass

class AnnotationNode(TerminalNode, InvisibleRole, BodyComponent):
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
class ShowBlockNode(TerminalNode, VisibleRole, BodyComponent):
    pass

# content 是不包括花括号的python代码体
class CodeBlockNode(TerminalNode, InvisibleRole, BodyComponent):
    pass

class IfNode(NonTerminalNode, BranchRole):
    pass

class ElifNode(NonTerminalNode, BranchRole):
    pass

# self.condition 无意义
class ElseNode(NonTerminalNode, BranchRole):
    pass

class ForNode(NonTerminalNode, LoopRole):
    pass

class WhileNode(NonTerminalNode, LoopRole):
    pass

class BreakNode(TerminalNode, InvisibleRole):
    pass

class ContinueNode(TerminalNode, InvisibleRole):
    pass

class EmptyNode(NonTerminalNode):
    pass