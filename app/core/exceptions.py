
class BookShareBaseException(Exception):
    """Базовое исключение нашего приложения """

    def __init__(self, message: str, status_code: int = 400, detail: dict |None = None):
        self.message = message
        self.status_code = status_code
        self.detail =  detail or {}
        super().__init__(self.message) # Вспомнить что такое super


class AuthenticationError(BookShareBaseException):      #Пользователь не распознан
    """Ошибка аутентификации"""

    def __init__(self, message: str = "Authentication failed.", detail: dict |None = None):
        super().__init__(message, status_code=401, detail=detail)


class AuthorizationError(BookShareBaseException):
    """Ошибка авторизации (нет прав)"""
    def __init__(self, message: str = "Access denied.", detail: dict |None = None):
        super().__init__(message, status_code=403, detail=detail)


class ResourceNotFound(BookShareBaseException):
    """Не найден ресурс"""
    def __init__(self, resource: str = "Resource", detail: dict |None = None):
        message = f"{resource} not found."
        super().__init__(message, status_code=404, detail=detail)


class InternalServerError(BookShareBaseException):
    def __init__self(self, message: str = "Internal server error.", detail: dict |None = None):
        super().__init__(message, status_code=500, detail=detail)
