from core.constants.error_messages import ERROR_MESSAGES


class ApiException(Exception):

  def __init__(self, code: str, status_code: int):
    self.code = code
    self.detail = ERROR_MESSAGES.get(code, "Erreur inconnue")
    self.status_code = status_code

    super().__init__(self.detail)


class NotFoundApiException(ApiException):

  def __init__(self, code: str):
    super().__init__(code=code, status_code=404)


class ConflictApiException(ApiException):

  def __init__(self, code: str):
    super().__init__(code=code, status_code=409)