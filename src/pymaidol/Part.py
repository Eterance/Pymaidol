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
    

class PartRecognizor:
    def __init__(self) -> None:
        self.part_list:list[Part] = []
        self._current_line:int = 0
        self._current_line_index:int = 0
        self._current_total_index = 0
        self._current_part:Part = Part("", self._current_line, self._current_line_index, self._current_total_index)
        self._last_line_final_index = -1
        self._template:str = ""
    
    def _reset(self):
        self.part_list:list[Part] = []
        self._current_line:int = 0
        self._current_line_index:int = 0
        self._current_total_index = 0
        self._current_part:Part = Part("", self._current_line, self._current_line_index, self._current_total_index)
        self._last_line_final_index = -1
        self._template:str = ""
    
    def _end_current_part_at_last_char(self):
        self._current_part.end_line = self._current_line if self._current_line_index != 0 else self._current_line - 1
        self._current_part.end = self._current_line_index - 1 if self._current_line_index != 0 else self._last_line_final_index
        self._current_part.total_end = self._current_total_index - 1
        if self._current_part.content != "":
            self.part_list.append(self._current_part)
    
    def _end_current_part_at_this_char(self):
        self._current_part.end_line = self._current_line 
        self._current_part.end = self._current_line_index
        self._current_part.total_end = self._current_total_index
        if self._current_part.content != "":
            self.part_list.append(self._current_part)
    
    def _create_new_part_at_current_char(self):
        self._current_part = Part("", self._current_line, self._current_line_index, self._current_total_index)
    
    def _consume_current_char_index(self, steps:int=1):
        """
        如果当前字符被消耗了（追加到 self._current_part.content 中），那么就要调用本函数更新 self._current_line_index 和 current_total_index。
        """
        self._current_line_index += steps
        self._current_total_index += steps
    
    def _consume_current_char_index_with_new_line(self, steps:int=1):
        """
        如果当前字符被消耗了（追加到 self._current_part.content 中），并且当前字符是 \n，那么就要调用本函数更新 self._current_line 和 last_line_length。
        """
        self._consume_current_char_index(steps)
        self._last_line_final_index = self._current_line_index # 本行的长度，包括 \n
        self._current_line += 1
        self._current_line_index = 0
    
    def _new_part_foresee_and_pair(self, foresee_consume_count:int, pair_left:list[str], pair_right:list[str], type:PartTypeEnum, is_include_right:bool=True):
        """

        Args:
            consume_count (int): 第一次要被消费的字符数。注意是包括@和前瞻数，比如 @if{，那么 consume_count = 4; @，那么 consume_count = 1
            pair_left (str): _description_
            pair_right (str): _description_
        """
        self._end_current_part_at_last_char()
        self._create_new_part_at_current_char()
        self._current_part.type = type
        # 消费当前的 @ 和前瞻的词语
        # 一次吃多个字符
        self._current_part.content = f"{self._current_part.content}{self._template[self._current_total_index:self._current_total_index+foresee_consume_count]}"
        self._consume_current_char_index(foresee_consume_count)
        # 持续消费，直到匹配到右侧
        pair_finder = PairFinder(pair_left, pair_right)
        while(self._current_total_index < len(self._template)):
            pair_result = pair_finder.IsPair(self._template[self._current_total_index])
            if pair_result:
                if is_include_right:                    
                    self._current_part.content = f"{self._current_part.content}{self._template[self._current_total_index]}"
                    # 匹配到了右侧，结束当前 part
                    self._end_current_part_at_this_char()
                    self._consume_current_char_index()
                    self._create_new_part_at_current_char()
                else:
                    self._end_current_part_at_last_char()
                    self._create_new_part_at_current_char()
                break
            self._current_part.content = f"{self._current_part.content}{self._template[self._current_total_index]}"
            self._consume_current_char_index()
    
    def Recognize(self, template:str):
        self._reset()
        self._template = template
        while(self._current_total_index < len(self._template)):
            current_char = self._template[self._current_total_index]
            if current_char == '\n':
                # 每一个Text的换行都要新建一个 part
                self._current_part.content = f"{self._current_part.content}{current_char}"
                self._end_current_part_at_this_char()
                self._consume_current_char_index_with_new_line()
                self._create_new_part_at_current_char()
                
            # 注释符号，一直匹配到 \n 为止
            elif current_char == '#':
                self._new_part_foresee_and_pair(1, [], ['\n'], PartTypeEnum.Comment)
                
            # 可能的嵌入符号
            elif current_char == '@':
                # 尝试前瞻
                remaining:str = self._template[self._current_total_index+1:]
                # 前瞻也是@，那么就是转义为 @
                if remaining.startswith('@'):
                    # 第一个 @ 不追加到 self._current_part.content 中，直接消费掉
                    self._consume_current_char_index()
                    current_char = self._template[self._current_total_index]
                    # 直接追加第二个 @ 到 self._current_part.content 中，之后就不会触发嵌入符号的逻辑了
                    self._current_part.content = f"{self._current_part.content}{current_char}"
                    self._consume_current_char_index()
                    
                # 前瞻是 {，那么新建 part，匹配到 } 为止
                elif remaining.startswith('{'):
                    self._new_part_foresee_and_pair(2, ['{'], ['}'], PartTypeEnum.CodeBlock)
                
                # 前瞻是 (，那么新建 part，匹配到 ) 为止
                elif remaining.startswith('('):
                    self._new_part_foresee_and_pair(2, ['('], [')'], PartTypeEnum.ShowBlock)
                
                elif remaining.startswith('if('):
                    self._new_part_foresee_and_pair(4, ['('], [')'], PartTypeEnum.If)
                    
                elif remaining.startswith('elif('):
                    self._new_part_foresee_and_pair(6, ['('], [')'], PartTypeEnum.Elif)
                    
                elif remaining.startswith('for('):
                    self._new_part_foresee_and_pair(5, ['('], [')'], PartTypeEnum.For)
                    
                # 一直消费字符直至遇到空白符（空白符不包括在内）
                else:
                    self._new_part_foresee_and_pair(1, [], [' ', '\t', '\n', '\r'], PartTypeEnum.SingleKeyword, False)
                
            # 纯文本
            else:
                self._current_part.content = f"{self._current_part.content}{current_char}"
                self._consume_current_char_index()
        
        # 结束最后一个 part
        self._end_current_part_at_last_char()
        return self.part_list
    

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