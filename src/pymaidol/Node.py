from typing import Optional

class PartBase:
    def __init__(
        self, 
        line:int, 
        content:str, 
        start:int,
        end:int,
        total_start:int,
        total_end:int,) -> None:
        
        self.content = content
        self.line = line # 位于第几行
        self.start:int = start # 从本行的第几个字符开始
        self.end:int = end # 从本行的第几个字符结束
        self.total_start:int = total_start # 从从头开始的第几个字符开始
        self.total_end:int = total_end # 从从头开始的第几个字符结束
        
        self.father:Optional[PartBase] = None # 语法树上的父结点
        self.line_predecessor:Optional[PartBase] = None # 和本结点在同一行的前一个结点
        self.line_successor:Optional[PartBase] = None # 和本结点在同一行的后一个结点
        
        
        
    def __str__(self) -> str:
        return self.content
    
    def __repr__(self) -> str:
        return f"line: {self.line}, content: {self.content}"
    
class TerminalPart(PartBase):
    pass
    
class TextPart(TerminalPart):
    pass

class CodePart(TerminalPart):
    pass

class EmbedPart(TerminalPart):
    pass

class CommentPart(TerminalPart):
    pass

class NonTerminalPart(PartBase):
    def __init__(
        self, 
        line:int, 
        content:str, 
        start:int,
        end:int,
        total_start:int,
        total_end:int,) -> None:
        
        super.__init__(line, content, start, end, total_start, total_end)
        self.children:list[PartBase] = []
        
class IfPart(NonTerminalPart):
    pass



def PartRecognizor(template:str):
    line:int = 0
    start:int = 0
    end:int = 0
    total_start:int = 0
    total_end:int = 0
    
    for index, char in enumerate(template):
        if char == '\n':
            line += 1
            start = 0
            end = 0