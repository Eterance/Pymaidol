from enum import Enum


class AnnotationTypeEnum(Enum):
    pass

class SingleLineAnnotationTypeEnum(AnnotationTypeEnum):    
    Python:str = "#"
    C:str = "//"
    
class MultiLineAnnotationTypeEnum(AnnotationTypeEnum):
    PythonSingleQuotation:str = "'''"    
    PythonDoubleQuotation:str = '"""'
    C:str = "/*"
    Html:str = "<!--"
    
FULL_ANNOTATION_TYPE:list[AnnotationTypeEnum] = [
    SingleLineAnnotationTypeEnum.Python,
    SingleLineAnnotationTypeEnum.C,
    MultiLineAnnotationTypeEnum.PythonSingleQuotation,
    MultiLineAnnotationTypeEnum.PythonDoubleQuotation,
    MultiLineAnnotationTypeEnum.C,
    MultiLineAnnotationTypeEnum.Html
]
    