from abc import ABC, abstractmethod

from pythondelegate.event_handler import EventHandler

from pymaidol.Nodes import (AnnotationNode, BaseNode, BreakNode, CodeBlockNode,
                            ContinueNode, ElifNode, ElseNode, EmptyNode,
                            ForNode, IfNode, NonTerminalNode, ShowBlockNode,
                            TerminalNode, TextNode, WhileNode)


class TraverserBase(ABC):
    def __init__(self, tree_root:BaseNode):
        self.entered_BaseNode = EventHandler[BaseNode]()
        self.entered_TerminalNode = EventHandler[TerminalNode]()
        self.entered_NonTerminalNode = EventHandler[NonTerminalNode]()
        self.entered_TextNode = EventHandler[TextNode]()
        self.entered_AnnotationNode = EventHandler[AnnotationNode]()
        self.entered_ShowBlockNode = EventHandler[ShowBlockNode]()
        self.entered_CodeBlockNode = EventHandler[CodeBlockNode]()
        self.entered_IfNode = EventHandler[IfNode]()
        self.entered_ElifNode = EventHandler[ElifNode]()
        self.entered_ElseNode = EventHandler[ElseNode]()
        self.entered_ForNode = EventHandler[ForNode]()
        self.entered_WhileNode = EventHandler[WhileNode]()
        self.entered_BreakNode = EventHandler[BreakNode]()
        self.entered_ContinueNode = EventHandler[ContinueNode]()
        self.entered_EmptyNode = EventHandler[EmptyNode]()
        
        self.tree_root = tree_root
        
    def _event_invoke(self, node:BaseNode):
        if node is None:
            return
        if type(node) == BaseNode:
            self.entered_BaseNode(self, node)
        if type(node) == TerminalNode: 
            self.entered_TerminalNode(self, node)
        if type(node) == NonTerminalNode: 
            self.entered_NonTerminalNode(self, node)
        if type(node) == TextNode: 
            self.entered_TextNode(self, node)
        if type(node) == AnnotationNode: 
            self.entered_AnnotationNode(self, node)
        if type(node) == ShowBlockNode: 
            self.entered_ShowBlockNode(self, node)
        if type(node) == CodeBlockNode: 
            self.entered_CodeBlockNode(self, node)
        if type(node) == IfNode: 
            self.entered_IfNode(self, node)
        if type(node) == ElifNode: 
            self.entered_ElifNode(self, node)
        if type(node) == ElseNode: 
            self.entered_ElseNode(self, node)
        if type(node) == ForNode: 
            self.entered_ForNode(self, node)
        if type(node) == WhileNode: 
            self.entered_WhileNode(self, node)
        if type(node) == BreakNode: 
            self.entered_BreakNode(self, node)
        if type(node) == ContinueNode: 
            self.entered_ContinueNode(self, node)
        if type(node) == EmptyNode: 
            self.entered_EmptyNode(self, node)
    
    def traverse(self):
        self._recursive_traverse(self.tree_root)
    
    @abstractmethod
    def _recursive_traverse(self, node:BaseNode):
        pass


class PreOrderTraverser(TraverserBase):
    """
        先序（先根）遍历语法树。
    """
    # Override
    def _recursive_traverse(self, node:BaseNode):
        self._event_invoke(node)
        if isinstance(node, NonTerminalNode):
            for child in node.children:
                self._recursive_traverse(child)
        
class InOrderTraverser(TraverserBase):
    """
        中序（后根）遍历语法树。
    """
    # Override
    def _recursive_traverse(self, node:BaseNode):
        if isinstance(node, NonTerminalNode):
            for child in node.children:
                self._recursive_traverse(child)
        self._event_invoke(node)