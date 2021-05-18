class ResponseDTO:
    def __init__(self, status, content):
        self.status = status
        self.content = content

    def to_dict(self):
        return {
            "status": self.status,
            "content": self.content
        }
