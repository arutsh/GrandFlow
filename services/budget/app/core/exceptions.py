from shared.exceptions.exceptions import DomainError, PermissionDenied  # noqa F401


# class DomainError(Exception):
#     def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
#         self.message = message
#         self.status_code = status_code


# class PermissionDenied(Exception):
#     def __init__(
#         self, message: str = "Permission denied", status_code: int = status.HTTP_400_BAD_REQUEST
#     ):
#         self.message = message
#         self.status_code = status_code
