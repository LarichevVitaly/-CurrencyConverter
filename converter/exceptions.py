class ServerException(Exception):
    def __init__(self, message='Internal server error', code=500):
        self.message = message
        self.code = code

    def __str__(self):
        if self.message:
            return f"Error: {self.message}"
        else:
            return f"Error occured on request"


class BadRequestException(ServerException):
    def __init__(self, message='Bad request', code=400):
        super().__init__(message, code)


class NotFoundException(ServerException):
    def __init__(self, message='Not found', code=404):
        super().__init__(message, code)
