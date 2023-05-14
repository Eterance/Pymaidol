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
        return f"Start: {self.start_line}:{self.start}({self.total_start}), End: {self.end_line}:{self.end}({self.total_end}); {self.type.value}, {self.content}"
    

class PartTypeEnum(Enum):
    Text = "Text" # 默认类型
    If = "If"
    Elif = "Elif"
    For = "For"
    While = "While"
    CodeBlock = 'CodeBlock'
    ShowBlock = "ShowBlock"
    Comment = "Comment"
    Else = "Else"
    SingleKeyword = "SingleKeyword"
    

class PartRecognizor:
    def __init__(self) -> None:
        self.part_list:list[Part] = []
        self._current_line_index:int = 0
        self._current_chat_index_inline:int = 0
        self._current_char_index_total = 0 # 指的是当前未被消费的字符。如果当前字符被消费，则应该立即步进1.
        self._current_part:Part = Part("", self._current_line_index, self._current_chat_index_inline, self._current_char_index_total)
        self._last_line_final_char_index = -1
        self._template:str = ""
    
    def _reset(self):
        self.part_list:list[Part] = []
        self._current_line_index:int = 0
        self._current_chat_index_inline:int = 0
        self._current_char_index_total = 0
        self._current_part:Part = Part("", self._current_line_index, self._current_chat_index_inline, self._current_char_index_total)
        self._last_line_final_char_index = -1
        self._template:str = ""
    
    def _end_current_part_at_last_char(self):
        self._current_part.end_line = self._current_line_index if self._current_chat_index_inline != 0 else self._current_line_index - 1
        self._current_part.end = self._current_chat_index_inline - 1 if self._current_chat_index_inline != 0 else self._last_line_final_char_index
        self._current_part.total_end = self._current_char_index_total - 1
        if self._current_part.content != "":
            self.part_list.append(self._current_part)
    
    def _end_current_part_at_this_char(self):
        self._current_part.end_line = self._current_line_index 
        self._current_part.end = self._current_chat_index_inline
        self._current_part.total_end = self._current_char_index_total
        if self._current_part.content != "":
            self.part_list.append(self._current_part)
    
    def _create_new_part_at_current_char(self):
        self._current_part = Part("", self._current_line_index, self._current_chat_index_inline, self._current_char_index_total)
    
    def _consume_current_char_index(self, steps:int=1):
        """
        如果当前字符被消耗了（追加到 self._current_part.content 中），
        那么就要调用本函数更新 self._current_line_index 和 current_total_index。
        会自动处理换行逻辑。
        """
        if self._template[self._current_char_index_total] == '\n':
            self._current_char_index_total += steps
            self._last_line_final_char_index = self._current_chat_index_inline # 本行的长度，包括 \n
            self._current_line_index += 1
            self._current_chat_index_inline = 0
        else:
            self._current_chat_index_inline += steps
            self._current_char_index_total += steps
    
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
        self._current_part.content = f"{self._current_part.content}{self._template[self._current_char_index_total:self._current_char_index_total+foresee_consume_count]}"
        self._consume_current_char_index(foresee_consume_count)
        # 持续消费，直到匹配到右侧
        pair_finder = PairFinder(pair_left, pair_right)
        while(self._current_char_index_total < len(self._template)):
            pair_result = pair_finder.IsPair(self._template[self._current_char_index_total])
            if pair_result:
                if is_include_right:                    
                    self._current_part.content = f"{self._current_part.content}{self._template[self._current_char_index_total]}"
                    # 匹配到了右侧，结束当前 part
                    self._end_current_part_at_this_char()
                    self._consume_current_char_index()
                    self._create_new_part_at_current_char()
                else:
                    self._end_current_part_at_last_char()
                    self._create_new_part_at_current_char()
                break
            self._current_part.content = f"{self._current_part.content}{self._template[self._current_char_index_total]}"
            self._consume_current_char_index()
    
    def _consume_continuous_char(self, char_list:list[str], add_into_current_part:bool=True):
        while (self._template[self._current_char_index_total] in char_list):
            if add_into_current_part:
                self._current_part.content = f"{self._current_part.content}{self._template[self._current_char_index_total]}"
                if self._template[self._current_char_index_total] == '\n':
                    pass
    
    def Recognize(self, template:str):
        self._reset()
        self._template = template
        while(self._current_char_index_total < len(self._template)):
            current_char = self._template[self._current_char_index_total]
            if current_char == '\n':
                # 每一个Text的换行都要新建一个 part
                self._current_part.content = f"{self._current_part.content}{current_char}"
                self._consume_current_char_index()
                self._end_current_part_at_last_char()
                self._create_new_part_at_current_char()
                
            # 注释符号，一直匹配到 \n 为止
            elif current_char == '#':
                self._new_part_foresee_and_pair(1, [], ['\n'], PartTypeEnum.Comment)
                
            # 可能的嵌入符号
            elif current_char == '@':
                # 尝试前瞻
                remaining:str = self._template[self._current_char_index_total+1:]
                # 前瞻也是@，那么就是转义为 @
                if remaining.startswith('@'):
                    # 第一个 @ 不追加到 self._current_part.content 中，直接消费掉
                    self._consume_current_char_index()
                    current_char = self._template[self._current_char_index_total]
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
    
    def _post_process(self):
        index = 0
        while (index < len(self.part_list)):
            current_part = self.part_list[index]
            # 校正单关键词的类型
            if current_part.type == PartTypeEnum.SingleKeyword:
                if current_part.content.startswith('@else'):
                    current_part.type = PartTypeEnum.Else
            
        

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