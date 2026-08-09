class TaskManagerException(Exception):
    """
    Base exception for all custom application errors.

    All custom exceptions in this application should inherit from this class,
    allowing a single except clause to catch any application-specific error.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistsError(TaskManagerException):
    """
    Raised when attempting to register a user with an email that already exists.
    """


class InvalidCredentialsError(TaskManagerException):
    """
    Raised when login credentials do not match any registered user.
    """


class TaskNotFoundError(TaskManagerException):
    """
    Raised when a requested task does not exist or does not belong to the user.
    """


class UnauthorizedAccessError(TaskManagerException):
    """
    Raised when a user attempts to access a resource they do not own.
    """
