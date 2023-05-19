from pymaidol.Errors import BranchError, ElseExtraConditionError, LackingConditionError
from pymaidol.Nodes import (BaseNode, BranchRole, ElifNode, ElseNode,
                            ForNode, IfNode, WhileNode)
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
        if node.condition is None:
            raise LackingConditionError(node.start)
        father = node.father
        assert father is not None
        index = father.children.index(node)
        index += 1
        previous = node
        while index < len(father.children):
            current = father.children[index]
            if not isinstance(current, (ElifNode, ElseNode)):
                break
            else:
                if isinstance(current, ElifNode) and current.condition is None:
                    raise LackingConditionError(current.start)
                if isinstance(current, ElseNode) and current.condition is not None:
                    raise ElseExtraConditionError(current.start)
                previous.next_branch = current
                current.previous_branch = previous
                previous = current
                # 本分支结点不再能从父结点进入，只能从上一个分支结点进入
                father.children.pop(index)
    
    def _loop_node_condition_check(self, sender:PreOrderTraverser, node:ForNode|WhileNode):
        if node.condition is None:
            raise LackingConditionError(node.start)
    
    def _wrong_branch_check(self, sender:PreOrderTraverser, node:BranchRole):
        # 所有的 elif 和 else 结点都被从父结点中移除了，只能从 if 进入
        # 如果触发这个方法，说明有游离的 elif 或 else 结点
        if isinstance(node, (ElifNode, ElseNode)):
            raise BranchError(node.start)
    
    # TODO: 检查 break 和 continue ，并找到对应的循环结点