from pymaidol.Errors import BranchError, ElseExtraConditionError, LackingConditionError
from pymaidol.Nodes import (BaseNode, BranchRole, ElifNode, ElseNode,
                            ForNode, IfNode, TextNode, WhileNode)
from pymaidol.Traversers import PreOrderTraverser


class SyntaxChecker():
    def __init__(self) -> None:
        pass
    
    def Check(self, root:BaseNode):        
        traverser = PreOrderTraverser(root)
        traverser.entered_IfNode += self._construct_if_branches
        traverser.entered_ForNode += self._loop_node_condition_check
        traverser.entered_WhileNode += self._loop_node_condition_check
        traverser.entered_BranchRole += self._wrong_branch_check
        
        traverser.traverse()
        
        traverser.entered_IfNode -= self._construct_if_branches
        traverser.entered_ForNode -= self._loop_node_condition_check
        traverser.entered_WhileNode -= self._loop_node_condition_check
        traverser.entered_BranchRole -= self._wrong_branch_check
        
        return root
    
    def _construct_if_branches(self, sender:PreOrderTraverser, node:IfNode):
        # 不知道为什么没有在初始化时拥有属性，因此在这里定义
        node.previous_branch = None
        node.next_branch = None
        if node.condition is None:
            raise LackingConditionError(node.start)
        father = node.father
        assert father is not None
        index = father.children.index(node)
        index += 1
        previous = node
        possible_gapping_whitespace_index:list[int] = []
        # 检查后续连续的 elif 和 else 结点，将它们构造成以 if 结点为头结点的链表
        while index < len(father.children):
            current = father.children[index]
            if isinstance(current, (ElifNode, ElseNode)):                
                current.previous_branch = None
                current.next_branch = None
                if isinstance(current, ElifNode) and current.condition is None:
                    raise LackingConditionError(current.start)
                if isinstance(current, ElseNode) and current.condition is not None:
                    raise ElseExtraConditionError(current.start)
                # 设置链表
                previous.next_branch = current
                current.previous_branch = previous
                previous = current                
                # 本分支结点不再能从父结点进入，只能从上一个分支结点进入                
                father.children.pop(index)
                # 倒序删除间隔的空白符
                for i in reversed(possible_gapping_whitespace_index):                   
                    father.children.pop(i)
                index -= len(possible_gapping_whitespace_index)
                possible_gapping_whitespace_index.clear()
                # else 后面不会再有分支结点，直接退出
                if isinstance(current, ElseNode):                    
                    break
            elif isinstance(current, TextNode):                
                if current.content.strip() == '':
                    # 虽然中间插了文本结点，但是全是空白符，可以忽略
                    possible_gapping_whitespace_index.append(index)
                    index += 1
                else:
                    break
            else:
                break
    
    def _loop_node_condition_check(self, sender:PreOrderTraverser, node:ForNode|WhileNode):
        if node.condition is None:
            raise LackingConditionError(node.start)
    
    def _wrong_branch_check(self, sender:PreOrderTraverser, node:BranchRole):
        # 所有的 elif 和 else 结点都被从父结点中移除了，只能从 if 进入
        # 如果触发这个方法，说明有游离的 elif 或 else 结点
        if isinstance(node, (ElifNode, ElseNode)):
            raise BranchError(node.start)