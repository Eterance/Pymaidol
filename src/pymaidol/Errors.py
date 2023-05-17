class BaseException(Exception):
    """Base class for all PML exceptions."""
    def __init__(self, line_index:int, line_char_index:int, total_index:int):
        self.line_index = line_index
        self.line_char_index = line_char_index
        self.total_index = total_index
        self._extra_detail:str = ""
        
    @property
    def Message(self):
        return f"{self.__class__.__name__} at Line {self.line_index}:{self.line_char_index}(total char index: {self.total_index}): Error Occur\n{self._extra_detail}"
    
    def __repr__(self) -> str:
        return self.Message
    
    def __str__(self) -> str:
        return self.Message
    
class UnexpectedTokenError(BaseException):
    def __init__(self, line_index: int, line_char_index: int, total_index: int, expected:list[str], got:str):
        super().__init__(line_index, line_char_index, total_index)
        self._expected:list[str] = expected
        self._got:str = got
        
    @property
    def Message(self):
        if len(self._expected) == 1:
            expected_string = f'"{self._expected[0]}"'
        else:
            expected_string = f'{self._expected}'
        return f'{self.__class__.__name__} at Line {self.line_index}:{self.line_char_index}(total char index: {self.total_index}): Expected {expected_string}, but got {self._got}\n{self._extra_detail}'
    
class ImpossibleError(Exception):
    pass