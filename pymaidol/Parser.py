from enum import Enum
from typing import Optional, Union

from pymaidol.AnnotationType import (AnnotationTypeEnum, FULL_ANNOTATION_TYPE,
                                MultiLineAnnotationTypeEnum,
                                SingleLineAnnotationTypeEnum)
from pymaidol.Errors import (MultiLineAnnotationFormatError, UnexpectedTokenError,
                    UnknownEmbedIdentifierError)
from pymaidol.keywords import (KeywordsEnum, NonTerminalKeywords, TerminalKeywords,
                      TranslateKeywords2Type)
from pymaidol.Nodes import (AnnotationNode, BaseNode, BodyComponent, CodeBlockNode,
                   EmptyNode, NonTerminalNode, ShowBlockNode, TerminalNode,
                   TextNode, VisibleRole)
from pymaidol.Positions import Position
from pymaidol.Traversers import PreOrderTraverser


class Parser:
    def __init__(
        self, 
        template:str, 
        root_node:Optional[NonTerminalNode]=None, 
        start:Position = Position.Default(), 
        end:Optional[Position] = None
        ) -> None:
        # 指的是当前未被消费的字符的位置。如果当前字符被消费，则应该立即步进1.
        self._current_position:Position = start
        # end 的行号和行内字符序号不重要
        self._end:Position = end if end is not None else Position(0, 0, len(template)-1)
        self.root = root_node if root_node else EmptyNode(0, 0, 0)
        self._current_node:BaseNode = TextNode(self._current_position, father=self.root)
        self._last_line_final_char_index = -1
        self.template:str = template
        self.__used = False
        # 用于记录当前行是否有可见字符。注意：“当前行”的定义是当前 node 的 start 所在行，而不是当前字符所在行。
        self._is_line_of_current_start_has_visible_content = False
        
        self.clean_trailing_whitespaces:bool = True
        self.supported_annotation_types:'list[AnnotationTypeEnum]' = FULL_ANNOTATION_TYPE
    
    @property
    def _current_char(self):
        return self.template[self._current_position.total]
    
    def _peek_several(self, char_count):
        end = self._current_position.total + char_count
        return self.template[self._current_position.total:end]
    
    @property
    def _remains(self):
        return self.template[self._current_position.total+1:]
    
    @property
    def _remains_include_current_char(self):
        return self.template[self._current_position.total:]
    
    def _detect_annotation(self):
        """
        检测注释类型。如果当前字符不是注释，则返回None，否则返回注释类型（注释的开始符）和注释的结束符。
        Args:
            support_annotation_types (list[AnnotationType], optional): 支持被检测的注释类型。默认为所有注释类型。
        """
        supported_annotation_types = self.supported_annotation_types
        if SingleLineAnnotationTypeEnum.Python in supported_annotation_types:
            if self._remains_include_current_char.startswith(SingleLineAnnotationTypeEnum.Python.value):
                return SingleLineAnnotationTypeEnum.Python, '\n'
        if SingleLineAnnotationTypeEnum.C in supported_annotation_types:
            if self._remains_include_current_char.startswith(SingleLineAnnotationTypeEnum.C.value):
                return SingleLineAnnotationTypeEnum.C, '\n'
        if MultiLineAnnotationTypeEnum.PythonDoubleQuotation in supported_annotation_types:
            if self._remains_include_current_char.startswith(MultiLineAnnotationTypeEnum.PythonDoubleQuotation.value):
                return MultiLineAnnotationTypeEnum.PythonDoubleQuotation, '"""'
        if MultiLineAnnotationTypeEnum.PythonSingleQuotation in supported_annotation_types:
            if self._remains_include_current_char.startswith(MultiLineAnnotationTypeEnum.PythonSingleQuotation.value):
                return MultiLineAnnotationTypeEnum.PythonSingleQuotation, "'''"
        if MultiLineAnnotationTypeEnum.C in supported_annotation_types:
            if self._remains_include_current_char.startswith(MultiLineAnnotationTypeEnum.C.value):
                return MultiLineAnnotationTypeEnum.C, '*/'
        if MultiLineAnnotationTypeEnum.Html in supported_annotation_types:
            if self._remains_include_current_char.startswith(MultiLineAnnotationTypeEnum.Html.value):
                return MultiLineAnnotationTypeEnum.Html, '-->'
        return None
    
    def _process_annotation(self, start_sign:AnnotationTypeEnum, end_sign:str):
        self._end_current_node_at_last_char()
        self._create_new_node_at_current_char(AnnotationNode, annotation_type=start_sign)
        assert isinstance(self._current_node, AnnotationNode)
        # 消费开始符
        self._current_node.append_content(start_sign.value)
        self._consume_current_char_index(len(start_sign.value))
        # 匹配注释体
        self._current_node.body, _, _ = self._consume_and_pair("", end_sign)
        # 多行注释时，检查注释结束符后面是否有除了空白字符以外的字符
        # 有则报错
        if isinstance(start_sign, MultiLineAnnotationTypeEnum):
            whitespace_peek, after_whitespace_peek = self._peek_while([' ', '\t'])
            if not after_whitespace_peek.startswith('\n'):
                raise MultiLineAnnotationFormatError(self._current_position)
            else:
                # 空白和换行符也算在多行注释里
                self._current_node.append_content(f"{whitespace_peek}\n")
                self._consume_current_char_index(len(whitespace_peek) + 1)
        # 清除前导空白符（如果这一行前面没有其他东西，也就是有缩进）
        if len(self.root.children) > 0 \
            and self.root.children[-1].start.line_index == self._current_node.start.line_index \
            and self.root.children[-1].content.strip() == "":
            #self._current_node.content = f"{self._root.children[-1].content}{self._current_node.content}"
            self._current_node.start = self.root.children[-1].start
            self.root.children.pop()
        # 如果上一个结点结束行和当前注释结点的起始相同（也就是注释不是开始于单独一行），则在上一个结点最后面加一个回车
        if len(self.root.children) > 0 and self.root.children[-1].end.line_index == self._current_node.start.line_index:
            self.root.children[-1].append_content('\n')
        # 结束
        self._end_current_node_at_last_char()
        self._create_new_node_at_current_char()
    
    def _end_current_node_at_last_char(self):
        end_line = self._current_position.line_index if self._current_position.char_index != 0 else self._current_position.line_index - 1
        end = self._current_position.char_index - 1 if self._current_position.char_index != 0 else self._last_line_final_char_index
        total_end = self._current_position.total - 1
        self._current_node.end = Position(end_line, end, total_end)
        if self._current_node.content != "":
            self.root.children.append(self._current_node)
            if isinstance(self._current_node, VisibleRole):
                self._is_line_of_current_start_has_visible_content = True
    
    def _end_current_part_at_this_char(self):
        end_line = self._current_position.line_index
        end = self._current_position.char_index
        total_end = self._current_position.total
        self._current_node.end = Position(end_line, end, total_end)
        if self._current_node.content != "":
            self.root.children.append(self._current_node)
            if isinstance(self._current_node, VisibleRole):
                self._is_line_of_current_start_has_visible_content = True
    
    def _create_new_node_at_current_char(self, type:type[BaseNode]=TextNode, **kwargs):
        self._current_node = type(
            start_position=self._current_position,
            father=self.root,
            **kwargs)
    
    def _consume_current_char_index(self, steps:int=1):
        """
        如果当前字符被消耗了（追加到 self._current_part.content 中），
        那么就要调用本函数更新 self._current_line_index 和 current_total_index。
        会自动处理换行逻辑。
        """
        if steps < 1:
            raise ValueError("steps must be greater than 0")
        for _ in range(steps):
            if self._current_char == '\n':
                self._last_line_final_char_index = self._current_position.char_index # 本行的长度，包括 \n
                self._current_position = Position(
                    self._current_position.line_index + 1, 
                    0, 
                    self._current_position.total + 1
                )
            else:
                self._current_position = Position(
                    self._current_position.line_index, 
                    self._current_position.char_index + 1, 
                    self._current_position.total + 1
                )
    
    def _consume_and_pair(
        self, 
        pair_left:str, 
        pair_right:str, 
        is_include_right:bool=True,
        suppress_unpaired_error:bool = False
        ):
        """

        Args:
            pair_left (str):
            pair_right (str):
        """
        # TODO: 处理左右长度不相等的情况
        # 持续消费，直到匹配到右侧
        content_start = self._current_position
        content_end = content_start
        pair_step = len(pair_right)
        content_inside = ""
        pair_finder = PairFinder(pair_left, pair_right)
        while(self._current_position.total < len(self.template)):
            pair_result = pair_finder.IsPair(self._peek_several(pair_step))
            if pair_result:
                if is_include_right:                    
                    self._current_node.content = f"{self._current_node.content}{self._peek_several(pair_step)}"
                    self._consume_current_char_index(pair_step)
                break
            content_inside = f"{content_inside}{self._current_char}"
            self._current_node.content = f"{self._current_node.content}{self._current_char}"
            content_end = self._current_position
            self._consume_current_char_index()
        if pair_finder.unpaired_left_count > 0 and not suppress_unpaired_error:
            # TODO: 报错未匹配的起始位置
            raise Exception(f"Unpaired left {pair_finder.unpaired_left_count} in template {self.template}")
        return content_inside, content_start, content_end
    
    def _new_node_foresee_and_pair(
            self, 
            foresee_consume_count:int, 
            pair_left:str, 
            pair_right:str, 
            node_type:type[NonTerminalNode|AnnotationNode], 
            is_include_right:bool=True,
            is_clean_whitespace:bool=True):
        
        self._end_current_node_at_last_char()
        self._create_new_node_at_current_char(node_type)
        assert isinstance(self._current_node, BodyComponent)
        # 消费当前的 @ 和前瞻的词语
        # 一次吃多个字符
        self._current_node.content = f"{self._current_node.content}{self._peek_several(foresee_consume_count)}"
        self._consume_current_char_index(foresee_consume_count)
        # 匹配
        self._current_node.body, _, _ = self._consume_and_pair(pair_left, pair_right, is_include_right)
        # 结束
        if is_clean_whitespace == True:
            self._try_discard_continuous_whitespaces_with_linefeed()
        self._end_current_node_at_last_char()
        self._create_new_node_at_current_char()
        
    def _add_and_consume_continuous_char(
        self, 
        char_list:list[str], 
        add_into_current_part:bool=True
        ):
        while (self._current_char in char_list):
            if add_into_current_part:
                self._current_node.content = f"{self._current_node.content}{self._current_char}"
            self._consume_current_char_index()
            
    def _peek_until(
        self, 
        until_char_list:list[str]=[' ', '\t', '\n', '\r', '(', ')', '{', '}', '[', ']', '"', "'", '`', '@', '#', '$', '%', '^', '&', '*', '-', '+', '=', '|', '\\', '/', '?', '<', '>', ',', '.', ';', ':', '!'],
        include_current_chat:bool=False
        ):
        start = self._current_position.total if include_current_chat else self._current_position.total+1
        remaining:str = self.template[start:]
        _index = 0
        _peeked = ""
        while (_index < len(remaining)):
            if remaining[_index] in until_char_list:
                break
            _peeked = f"{_peeked}{remaining[_index]}"
            _index += 1
        after_peek = remaining[_index:]
        return _peeked, after_peek
    
    def _peek_while(
        self, 
        char_list:list[str],
        include_current_chat:bool=True
        ):
        start = self._current_position.total if include_current_chat else self._current_position.total+1
        remaining:str = self.template[start:]
        _index = 0
        _peeked = ""
        while (_index < len(remaining)):
            if remaining[_index] not in char_list:
                break
            _peeked = f"{_peeked}{remaining[_index]}"
            _index += 1
        after_peek = remaining[_index:]
        return _peeked, after_peek
    
    def _peek_while_from_tail(
        self, 
        string:str,
        char_list:list[str],
        ):
        _index = len(string)-1
        _peeked = ""
        while (_index >= 0):
            if string[_index] not in char_list:
                break
            _peeked = f"{string[_index]}{_peeked}"
            _index -= 1
        after_peek = string[:_index+1]
        return _peeked, after_peek
        
    def _non_terminal_keyword_check_type(self):
        """
        检查剩余的字符串是否以 char_list 中的任意一个开头
        """
        _peek, _ = self._peek_until([' ', '\t', '\n', '\r', '(', ')', '{', '}', '[', ']', '"', "'", '`', '@', '#', '$', '%', '^', '&', '*', '-', '+', '=', '|', '\\', '/', '?', '<', '>', ',', '.', ';', ':', '!'])
        for keyword_type in NonTerminalKeywords:
            if _peek == keyword_type.value:
                return keyword_type
        return None
    
    def _terminal_keyword_check_type(self):
        """
        检查剩余的字符串是否以 char_list 中的任意一个开头
        """
        _peek, _ = self._peek_until([';'])
        for keyword_type in TerminalKeywords:
            if _peek == keyword_type.value:
                return keyword_type
        return None
    
    def _is_continuous_whitespaces_until_linefeed(self):
        whitespace_peek, after_whitespace_peek = self._peek_while([' ', '\t'])
        if after_whitespace_peek.startswith('\n'):
            return True
        else:
            return False
    
    def _try_discard_continuous_whitespaces_with_linefeed(self):
        """试图清除从当前位置开始的连续的空白符，直到遇到换行符为止。如果该行有内容，则不会清除任何空白符。
        """
        whitespace_peek, after_whitespace_peek = self._peek_while([' ', '\t'])
        if after_whitespace_peek.startswith('\n'):
            # 抛弃左大括号后跟的掉空白符以及第一个换行符，也就是等于将body的第一行放到左大括号后面
            self._consume_current_char_index(len(whitespace_peek)+1)
    
    def _is_leading_continuous_whitespaces(self):
        if len(self.root.children) > 0 \
            and isinstance(self.root.children[-1], TextNode) \
            and self.root.children[-1].content.strip() == "" \
            and self.root.children[-1].start.line_index == self._current_node.start.line_index \
            and self.root.children[-1].start.char_index == 0 \
            :
            return True
        else:
            return False
        
    def _try_discard_leading_continuous_whitespaces(self):
        # 清除当前 node 的行首前导空白符
        # 上一个 text 结点是当前结点的前导空白符的判断标准：
        # 1. 上一个结点是 TextNode，并且全是空白符
        # 2. 上一个结点的 start 位置和当前结点的 start 位置在同一行
        # 3. 上一个结点是从行首开始计数的（start.char_index == 0）
        if len(self.root.children) > 0 \
            and isinstance(self.root.children[-1], TextNode) \
            and self.root.children[-1].content.strip() == "" \
            and self.root.children[-1].start.line_index == self._current_node.start.line_index \
            and self.root.children[-1].start.char_index == 0 \
            :
            self._is_line_of_current_start_has_visible_content = False
            self._current_node.start = self.root.children[-1].start
            self.root.children.pop()
        
    def _non_terminal_node_parse(self, keyword_type:KeywordsEnum):
        self._end_current_node_at_last_char()
        self._create_new_node_at_current_char(TranslateKeywords2Type(keyword_type))
        assert isinstance(self._current_node, NonTerminalNode)
        # 消费@关键词
        self._current_node.content = f"{self._current_node.content}{self._current_char}{keyword_type.value}"
        self._consume_current_char_index(len(keyword_type.value)+1)
        
        peek, after_peek = self._peek_while([' ', '\t'], True)
        # 以左圆括号开头，说明有条件
        if after_peek.startswith('('):
            # 关键词与左圆括号之间的空白符，和左圆括号全部消费
            self._current_node.append_content(f"{peek}(")
            self._consume_current_char_index(len(peek)+1)
            # 消费后，当前的字符应该是左圆括号后的条件表达式的第一个字符
            self._current_node.condition, _, _ = self._consume_and_pair('(', ')', is_include_right=False)
            # 消费右圆括号  
            self._current_node.append_content(f")")      
            self._consume_current_char_index()
        
        peek, after_peek = self._peek_while([' ', '\t', '\n', '\r'], True)
        # 以左大括号开头，说明有 body
        if after_peek.startswith('{'):
            # 关键词与左大括号之间的空白符、换行符，和左大括号全部消费            
            self._current_node.append_content(peek + "{")
            self._consume_current_char_index(len(peek)+1)
            # 抛弃左大括号后跟的掉空白符以及第一个换行符，也就是等于将body的第一行放到左大括号后面
            # 消费后，当前的字符应该是左大括号后的body的第一个字符
            self._try_discard_continuous_whitespaces_with_linefeed()
            self._current_node.body, body_start, body_end = self._consume_and_pair('{', '}', is_include_right=False)
            # 如果右括号单独一行，清除右大括号前的空白符，遇到换行符停止（不清除换行符）
            is_right_brace_start_of_new_line = False
            whitespace, after_whitespace_peek = self._peek_while_from_tail(self._current_node.body, [' ', '\t'])
            if after_whitespace_peek.endswith('\n'):
                is_right_brace_start_of_new_line = True
                self._current_node.body = after_whitespace_peek
                body_end = Position(body_end.line_index, body_end.char_index-len(whitespace), body_end.total-len(whitespace))
            # 右大括号
            self._current_node.append_content("}")
            self._consume_current_char_index()
            
            # 处理子结点
            sub_parser = Parser(self.template, self._current_node, body_start, body_end)
            sub_parser.clean_trailing_whitespaces = False
            sub_parser.Parse()
            
            # 如果子结点都是不可见，并且本分支结点单独一行；           
            # 或者如果右括号单独一行, 清除右大括号后的空白符，遇到第一个换行符停止（清除换行符）
            if (self._is_children_have_visible_content(self._current_node) == False\
                and self._current_node.start.line_index == self._current_position.line_index)\
                or is_right_brace_start_of_new_line == True:
                self._try_discard_continuous_whitespaces_with_linefeed()
            
            self._end_current_node_at_last_char()
            self._create_new_node_at_current_char()
        else:
            raise UnexpectedTokenError(self._current_position, ['{'], after_peek[0])
        
    def _is_children_have_visible_content(self, node:NonTerminalNode):
        for child in node.children:
            if isinstance(child, VisibleRole):
                return True
            elif isinstance(child, NonTerminalNode) and self._is_children_have_visible_content(child):
                return True
        return False
    
    def _terminal_keyword_process(self, keyword_type:KeywordsEnum):
        self._end_current_node_at_last_char()
        self._create_new_node_at_current_char(TranslateKeywords2Type(keyword_type))
        assert isinstance(self._current_node, TerminalNode)
        # 消费@关键词
        # self._current_char is '@'
        self._current_node.content = f"{self._current_node.content}{keyword_type.value}"
        self._consume_current_char_index(len(keyword_type.value)+1)
        # 消费掉分号
        self._consume_current_char_index()
        # 如果这一行只有终结符关键字，清除前导后随空白符和换行
        if self._is_leading_continuous_whitespaces()\
            and self._is_continuous_whitespaces_until_linefeed():
            
            self._try_discard_leading_continuous_whitespaces()
            self._try_discard_continuous_whitespaces_with_linefeed()
        
        self._end_current_node_at_last_char()
        self._create_new_node_at_current_char()
    
    def Parse(self):
        if self.__used == True:
            raise Exception("Parser can only be used once.")
        while(self._current_position.total <= self._end.total):
            if self._current_char == '\n':
                # 每一个Text的换行都要新建一个 part
                self._current_node.content = f"{self._current_node.content}{self._current_char}"
                self._consume_current_char_index()
                self._end_current_node_at_last_char()
                self._create_new_node_at_current_char()
                self._is_line_of_current_start_has_visible_content = False
            
            # 注释处理
            elif (_detect_result := self._detect_annotation()) is not None:
                start_type, end_sign = _detect_result
                self._process_annotation(start_type, end_sign)
            
            # 可能的嵌入符号
            elif self._current_char == '@':
                # 前瞻也是@，那么就是转义为 @
                if self._remains.startswith('@'):
                    # 第一个 @ 不追加到 self._current_part.content 中，直接消费掉
                    self._consume_current_char_index()
                    # 直接追加第二个 @ 到 self._current_part.content 中，之后就不会触发嵌入符号的逻辑了
                    self._current_node.content = f"{self._current_node.content}{self._current_char}"
                    self._consume_current_char_index()
                    
                # 前瞻是 {，那么新建 part，匹配到 } 为止
                elif self._remains.startswith('{'):
                    self._new_node_foresee_and_pair(2, '{', '}', CodeBlockNode)
                
                # 前瞻是 (，那么新建 part，匹配到 ) 为止
                elif self._remains.startswith('('):
                    self._new_node_foresee_and_pair(2, '(', ')', ShowBlockNode, is_clean_whitespace=False)
                                    
                elif (keyword_type := self._non_terminal_keyword_check_type()) is not None:
                    self._non_terminal_node_parse(keyword_type)
                
                elif (keyword_type := self._terminal_keyword_check_type()) is not None:
                    # 处理主体
                    self._terminal_keyword_process(keyword_type)
                
                # 未知的嵌入符号
                else:
                    _peek_identifier, _ = self._peek_until([' ', '\t', '\n', '\r', '(', ')', '{', '}', '[', ']', '"', "'", '`', '@', '#', '$', '%', '^', '&', '*', '-', '+', '=', '|', '\\', '/', '?', '<', '>', ',', '.', ';', ':', '!'])
                    raise UnknownEmbedIdentifierError(self._current_position, _peek_identifier)
                
            # 纯文本
            else:
                self._current_node.content = f"{self._current_node.content}{self._current_char}"
                self._consume_current_char_index()
        
        # 结束最后一个 part
        self._end_current_node_at_last_char()
        self.__used = True
        self._post_process()
        return self.root
    
    def _post_process(self):
        if self.clean_trailing_whitespaces == True:
            traverser = PreOrderTraverser(self.root)
            traverser.entered_TextNode += self._delete_trailing_whitespaces
            traverser.traverse()
            traverser.entered_TextNode -= self._delete_trailing_whitespaces
            
    def _delete_trailing_whitespaces(self, sender:PreOrderTraverser, text_node:TextNode):
        cleaned = ""
        index = len(text_node.content) - 1
        kill_whitespace = False
        while index >= 0:
            if text_node.content[index] == '\n':
                cleaned = f"{text_node.content[index]}{cleaned}"
                kill_whitespace = True
            elif kill_whitespace == True and text_node.content[index] in [' ', '\t']:
                pass
            else:
                cleaned = f"{text_node.content[index]}{cleaned}"
                kill_whitespace = False
            index -= 1
        text_node.content = cleaned

class PairFinder():
    def __init__(self, left:str, right:str) -> None:
        self.unpaired_left_count = 0
        self.__left = left
        self.__right = right
    
    def IsPair(self, target:str):
        if target == self.__left:
            self.unpaired_left_count += 1
            return False
        elif target == self.__right:
            if self.unpaired_left_count == 0:
                return True
            else:
                self.unpaired_left_count -= 1
                return False
        else:
            return False