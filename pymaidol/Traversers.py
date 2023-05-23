from abc import ABC, abstractmethod

from pythondelegate.event_handler import EventHandler

from pymaidol.Nodes import (AnnotationNode, BaseNode, BodyComponent, BranchRole,
                    BreakNode, CodeBlockNode, ComponentOrRole, ContinueNode,
                    ElifNode, ElseNode, EmptyNode, ForNode, IfNode,
                    InvisibleRole, LoopRole, NonTerminalNode, ShowBlockNode,
                    TerminalNode, TextNode, VisibleRole, WhileNode)


class TraverserBase(ABC):
    def __init__(self, tree_root:BaseNode, is_trigger_father_class_event:bool=True):
        """ The base class of all traversers. It provides a series of events that can be triggered when traversing the tree. The event is triggered when the node is entered. The event is triggered in the order of the inheritance chain of the node class. 
        
        Args:
            tree_root (BaseNode): The root node of the tree to be traversed.
            is_trigger_father_class_event (bool, optional): Whether to trigger the event of the parent class. Defaults to True. For example, if current node is a TextNode and this parameter is False, then the event of TerminalNode will not be triggered. Defaults to True.
        """
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
        
        self.entered_BranchRole = EventHandler[BranchRole]()
        self.entered_ComponentOrRole = EventHandler[ComponentOrRole]()
        self.entered_VisibleRole = EventHandler[VisibleRole]()
        self.entered_InvisibleRole = EventHandler[InvisibleRole]()
        self.entered_BodyComponent = EventHandler[BodyComponent]()
        self.entered_LoopRole = EventHandler[LoopRole]()
        
        self.tree_root = tree_root
        self.is_trigger_father_class_event = is_trigger_father_class_event
        
    def _entered_event_invoke(self, node:BaseNode):
        if node is None:
            return
        # TerminalNode
        if type(node) == TextNode: 
            self.entered_TextNode(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == AnnotationNode: 
            self.entered_AnnotationNode(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == ShowBlockNode: 
            self.entered_ShowBlockNode(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == CodeBlockNode: 
            self.entered_CodeBlockNode(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == BreakNode: 
            self.entered_BreakNode(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == ContinueNode: 
            self.entered_ContinueNode(self, node)
            if self.is_trigger_father_class_event: return
            
        # NonTerminalNode
        if type(node) == IfNode: 
            self.entered_IfNode(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == ElifNode: 
            self.entered_ElifNode(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == ElseNode: 
            self.entered_ElseNode(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == ForNode: 
            self.entered_ForNode(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == WhileNode: 
            self.entered_WhileNode(self, node)     
            if self.is_trigger_father_class_event: return   
        if type(node) == EmptyNode: 
            self.entered_EmptyNode(self, node)
            if self.is_trigger_father_class_event: return
        
        # VirtualNode
        if type(node) == TerminalNode: 
            self.entered_TerminalNode(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == NonTerminalNode: 
            self.entered_NonTerminalNode(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == BaseNode:
            self.entered_BaseNode(self, node)
            if self.is_trigger_father_class_event: return
            
        # ComponentNode
        if type(node) == LoopRole: 
            self.entered_LoopRole(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == BranchRole: 
            self.entered_BranchRole(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == BodyComponent: 
            self.entered_BodyComponent(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == InvisibleRole: 
            self.entered_InvisibleRole(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == VisibleRole: 
            self.entered_VisibleRole(self, node)
            if self.is_trigger_father_class_event: return
        if type(node) == ComponentOrRole: 
            self.entered_ComponentOrRole(self, node)
            if self.is_trigger_father_class_event: return
    
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
        self._entered_event_invoke(node)
        if isinstance(node, NonTerminalNode):
            index = 0
            # 由于在遍历过程中可能会修改children，所以不能使用for循环
            while index < len(node.children):
                current_node = node.children[index]
                self._recursive_traverse(current_node)
                try:
                    index = node.children.index(current_node)
                except:
                    pass
                index += 1
        
class InOrderTraverser(TraverserBase):
    """
        中序（后根）遍历语法树。
    """
    # Override
    def _recursive_traverse(self, node:BaseNode):        
        if isinstance(node, NonTerminalNode):
            index = 0
            # 由于在遍历过程中可能会修改children，所以不能使用for循环
            while index < len(node.children):
                current_node = node.children[index]
                self._recursive_traverse(current_node)
                try:
                    index = node.children.index(current_node)
                except:
                    pass
                index += 1
        self._entered_event_invoke(node)