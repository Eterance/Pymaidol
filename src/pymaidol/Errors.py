class BaseException(Exception):
    """Base class for all PML exceptions."""
    def __init__(self, line_index:int, line_char_index:int, total_index:int):
        self.line_index = line_index
        self.line_char_index = line_char_index
        self.total_index = total_index
        self.extra_detail:str = ""
        
    @property
    def Message(self):
        return f"{self.__class__.__name__} at Line {self.line_index}:{self.line_char_index}(total char index: {self.total_index}): Error Occur\n{self.extra_detail}"
    
    def __repr__(self) -> str:
        return self.Message
    
    def __str__(self) -> str:
        return self.Message
    
class UnexpectedTokenError(BaseException):
    def __init__(self, line_index: int, line_char_index: int, total_index: int, expected:list[str], got:str):
        super().__init__(line_index, line_char_index, total_index)
        self.expected:list[str] = expected
        self.got:str = got
        
    @property
    def Message(self):
        if len(self.expected) == 1:
            expected_string = f'"{self.expected[0]}"'
        else:
            expected_string = f'{self.expected}'
        return f'{self.__class__.__name__} at Line {self.line_index}:{self.line_char_index}(total char index: {self.total_index}): Expected {expected_string}, but got {self.got}\n{self.extra_detail}'

# Only use/happen in dev.
class ImpossibleError(Exception):
    pass

class MultiLineAnnotationFormatError(BaseException):
    @property
    def Message(self):
        return f"{self.__class__.__name__} at Line {self.line_index}:{self.line_char_index}(total char index: {self.total_index}): When using multi-line annotation, the line where the terminator is located must not have any text other than the annotation."
    
class UnknownEmbedIdentifierError(BaseException):
    def __init__(self, line_index: int, line_char_index: int, total_index: int, unknown_identifier:str):
        super().__init__(line_index, line_char_index, total_index)
        self.unknown_identifier:str = unknown_identifier
    
    @property
    def Message(self):
        return f'{self.__class__.__name__} at Line {self.line_index}:{self.line_char_index}(total char index: {self.total_index}): Unknown "@{self.unknown_identifier}". If you want to write "@" in template, use "@@" instead.'