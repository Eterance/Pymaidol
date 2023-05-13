from enum import Enum
from typing import Optional

class Part:
    def __init__(
        self, 
        content:str, 
        start_line:int, 
        start:int,
        total_start:int) -> None:
        
        self.content = content
        self.start_line = start_line 
        self.start:int = start # 从本行的第几个字符开始
        self.end_line = -1
        self.end:int = -1 # 从本行的第几个字符结束
        self.total_start:int = total_start # 从从头开始的第几个字符开始
        self.total_end:int = -1 # 从从头开始的第几个字符结束
        self.type:PartTypeEnum = PartTypeEnum.Text
        
    def __str__(self) -> str:
        return self.content
    
    def __repr__(self) -> str:
        return f"{self.type.value}, {self.content}"
    

class PartTypeEnum(Enum):
    Text = "Text" # 默认类型
    If = "If"
    Elif = "Elif"
    For = "For"
    CodeBlock = 'CodeBlock'
    ShowBlock = "ShowBlock"
    Comment = "Comment"
    SingleKeyword = "SingleKeyword"
    

def PartRecognizor(template:str):
    list_of_parts:list[Part] = []
    current_line:int = 0
    current_line_index:int = 0
    current_total_index = 0
    current_part:Part = Part("", current_line, current_line_index, current_total_index)
    last_line_final_index = -1
    
    def _end_current_part_at_last_char():
        nonlocal current_part, current_line, current_line_index, current_total_index
        current_part.end_line = current_line if current_line_index != 0 else current_line - 1
        current_part.end = current_line_index - 1 if current_line_index != 0 else last_line_final_index
        current_part.total_end = current_total_index - 1
        if current_part.content != "":
            list_of_parts.append(current_part)
        
    def _end_current_part_at_this_char():
        nonlocal current_part, current_line, current_line_index, current_total_index
        current_part.end_line = current_line 
        current_part.end = current_line_index
        current_part.total_end = current_total_index
        if current_part.content != "":
            list_of_parts.append(current_part)
    
    def _create_new_part_at_current_char():
        nonlocal current_part, current_line, current_line_index, current_total_index
        current_part = Part("", current_line, current_line_index, current_total_index)
    
    def _consume_current_char_index(steps:int=1):
        """
        如果当前字符被消耗了（追加到 current_part.content 中），那么就要调用本函数更新 current_line_index 和 current_total_index。
        """
        nonlocal current_line_index, current_total_index
        current_line_index += steps
        current_total_index += steps
    
    def _consume_current_char_index_with_new_line(steps:int=1):
        """
        如果当前字符被消耗了（追加到 current_part.content 中），并且当前字符是 \n，那么就要调用本函数更新 current_line 和 last_line_length。
        """
        nonlocal current_line, current_line_index, current_total_index, last_line_final_index, _consume_current_char_index
        _consume_current_char_index(steps)
        last_line_final_index = current_line_index # 本行的长度，包括 \n
        current_line += 1
        current_line_index = 0
        
    def _new_part_foresee_and_pair(foresee_consume_count:int, pair_left:list[str], pair_right:list[str], type:PartTypeEnum, is_include_right:bool=True):
        """_

        Args:
            consume_count (int): 第一次要被消费的字符数。注意是包括@和前瞻数，比如 @if{，那么 consume_count = 4; @，那么 consume_count = 1
            pair_left (str): _description_
            pair_right (str): _description_
        """
        nonlocal current_part, current_total_index, template
        _end_current_part_at_last_char()
        _create_new_part_at_current_char()
        current_part.type = type
        # 消费当前的 @ 和前瞻的词语
        # 一次吃多个字符
        current_part.content = f"{current_part.content}{template[current_total_index:current_total_index+foresee_consume_count]}"
        _consume_current_char_index(foresee_consume_count)
        # 持续消费，直到匹配到右侧
        pair_finder = PairFinder(pair_left, pair_right)
        while(current_total_index < len(template)):
            pair_result = pair_finder.IsPair(template[current_total_index])
            if pair_result:
                if is_include_right:                    
                    current_part.content = f"{current_part.content}{template[current_total_index]}"
                    # 匹配到了右侧，结束当前 part
                    _end_current_part_at_this_char()
                    _consume_current_char_index()
                    _create_new_part_at_current_char()
                else:
                    _end_current_part_at_last_char()
                    _create_new_part_at_current_char()
                break
            current_part.content = f"{current_part.content}{template[current_total_index]}"
            _consume_current_char_index()
    
    while(current_total_index < len(template)):
        current_char = template[current_total_index]
        if current_char == '\n':
            # 每一个Text的换行都要新建一个 part
            current_part.content = f"{current_part.content}{current_char}"
            _end_current_part_at_this_char()
            _consume_current_char_index_with_new_line()
            _create_new_part_at_current_char()
            
        # 注释符号，一直匹配到 \n 为止
        elif current_char == '#':
            _new_part_foresee_and_pair(1, [], ['\n'], PartTypeEnum.Comment)
            
        # 可能的嵌入符号
        elif current_char == '@':
            # 尝试前瞻
            remaining:str = template[current_total_index+1:]
            # 前瞻也是@，那么就是转义为 @
            if remaining.startswith('@'):
                # 第一个 @ 不追加到 current_part.content 中，直接消费掉
                _consume_current_char_index()
                current_char = template[current_total_index]
                # 直接追加第二个 @ 到 current_part.content 中，之后就不会触发嵌入符号的逻辑了
                current_part.content = f"{current_part.content}{current_char}"
                _consume_current_char_index()
                
            # 前瞻是 {，那么新建 part，匹配到 } 为止
            elif remaining.startswith('{'):
                _new_part_foresee_and_pair(2, ['{'], ['}'], PartTypeEnum.CodeBlock)
            
            # 前瞻是 (，那么新建 part，匹配到 ) 为止
            elif remaining.startswith('('):
                _new_part_foresee_and_pair(2, ['('], [')'], PartTypeEnum.ShowBlock)
            
            elif remaining.startswith('if('):
                _new_part_foresee_and_pair(4, ['('], [')'], PartTypeEnum.If)
                
            elif remaining.startswith('elif('):
                _new_part_foresee_and_pair(6, ['('], [')'], PartTypeEnum.Elif)
                
            elif remaining.startswith('for('):
                _new_part_foresee_and_pair(5, ['('], [')'], PartTypeEnum.For)
                
            # 一直消费字符直至遇到空白符（空白符不包括在内）
            else:
                _new_part_foresee_and_pair(1, [], [' ', '\t', '\n', '\r'], PartTypeEnum.SingleKeyword, False)
            
        # 纯文本
        else:
            current_part.content = f"{current_part.content}{current_char}"
            _consume_current_char_index()
    
    # 结束最后一个 part
    _end_current_part_at_last_char()
    return list_of_parts
        
class PairFinder():
    def __init__(self, left:list[str], right:list[str]) -> None:
        self.__unpaired_left_count = 0
        self.__left = left
        self.__right = right
    
    def IsPair(self, target:str):
        if target in self.__left:
            self.__unpaired_left_count += 1
            return False
        elif target in self.__right:
            if self.__unpaired_left_count == 0:
                return True
            else:
                self.__unpaired_left_count -= 1
                return False
        else:
            return False