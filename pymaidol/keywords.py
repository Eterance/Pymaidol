from enum import Enum

from pymaidol.Nodes import (AnnotationNode, BaseNode, BreakNode, CodeBlockNode,
                   ElifNode, ElseNode, ForNode, IfNode, NonTerminalNode,
                   ShowBlockNode, TerminalNode, TextNode, WhileNode)


class KeywordsEnum(Enum):
    If:str = "if"
    Elif:str = "elif"
    For:str = "for"
    While:str = "while"
    Else:str = "else"
    Break:str = "break"
    Continue:str = "continue"

# @readonly
TerminalKeywords = [
    KeywordsEnum.Break,
    KeywordsEnum.Continue
]

# @readonly
NonTerminalKeywords = [
    KeywordsEnum.If,
    KeywordsEnum.Elif,
    KeywordsEnum.For,
    KeywordsEnum.While,
    KeywordsEnum.Else
]

def TranslateKeywords2Type(keywordsEnum:KeywordsEnum):
    if keywordsEnum == KeywordsEnum.If:
        return IfNode
    elif keywordsEnum == KeywordsEnum.Elif: 
        return ElifNode
    elif keywordsEnum == KeywordsEnum.For: 
        return ForNode
    elif keywordsEnum == KeywordsEnum.While:
        return WhileNode
    elif keywordsEnum == KeywordsEnum.Else:
        return ElseNode
    elif keywordsEnum == KeywordsEnum.Break:
        return BreakNode
    elif keywordsEnum == KeywordsEnum.Continue:
        return BreakNode
    