class Position():
    def __init__(self, line_index:int, char_index:int, total:int) -> None:
        self.__line_index = line_index
        self.__char_index = char_index
        self.__char_index_total = total
    
    @property
    def line_index(self):
        return self.__line_index
    
    @property
    def char_index(self):
        return self.__char_index
    
    @property
    def total(self):
        return self.__char_index_total
    
    @classmethod
    def Default(cls):
        return cls(0, 0, 0)
    
    def Copy(self):
        return Position(self.__line_index, self.__char_index, self.__char_index_total)
    
    def __str__(self):
        return f"{self.line_index}:{self.char_index}({self.total})"
    
    @property
    def full_description(self):
        return f"line {self.line_index} char {self.char_index} (total {self.total})"
    
    def __repr__(self):
        return f"Position @{str(self)}"