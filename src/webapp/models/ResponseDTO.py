from enum import Enum


class ResponseTypeEnum(Enum):
    PROVED = "PROVED"
    NOT_PROVED = "NOT_PROVED"
    SYNTAX_ERROR = "SYNTAX_ERROR"


class ResponseDTO:
    def __init__(self, response_type: ResponseTypeEnum = ResponseTypeEnum.NOT_PROVED, content: [] = []):
        self.response_type = response_type
        self.content = content

    def to_dict(self):
        return {
            "response_type": self.response_type.value,
            "content": self.content
        }

    def set_response_type(self, response_type: ResponseTypeEnum):
        self.response_type = response_type

    def set_content(self, content):
        self.content = content
