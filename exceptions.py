from pysmshub.utils import get_system_language


class BaseSmsHubApiException(Exception):
    """Base exception class for SmsHubApi errors."""

    MESSAGES = {"en": "An error has occurred", "ru": "Произошла ошибка"}

    def __init__(self, message=None):
        lang = get_system_language()
        default_message = self.MESSAGES.get(lang, self.MESSAGES["en"])
        self.message = message or default_message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class SmsHubApiException(BaseSmsHubApiException):
    """Exception raised when the API returns an unexpected response."""

    MESSAGES = {
        "en": "Method {method} returned an unexpected response",
        "ru": "Метод {method} вернул неожиданный ответ",
    }

    def __init__(self, method, error):
        lang = get_system_language()
        message_template = self.MESSAGES.get(lang[:2], self.MESSAGES["en"])
        message = message_template.format(method=method)
        self.response = error
        super().__init__(f"{message}: {error}")


class ConnectionErrorException(BaseSmsHubApiException):
    """Exception raised when a network connection error occurs."""

    MESSAGES = {
        "en": "A network connection error occurred",
        "ru": "Произошла ошибка сетевого соединения",
    }

    def __init__(self):
        lang = get_system_language()
        message = self.MESSAGES.get(lang, self.MESSAGES["en"])
        super().__init__(message)
