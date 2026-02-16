"""自定义异常"""


class BusinessException(Exception):
    """业务异常基类"""
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationException(BusinessException):
    """数据验证异常"""
    def __init__(self, message: str):
        super().__init__(message, 400)


class AuthenticationException(BusinessException):
    """认证异常"""
    def __init__(self, message: str = "认证失败"):
        super().__init__(message, 401)


class PermissionException(BusinessException):
    """权限异常"""
    def __init__(self, message: str = "权限不足"):
        super().__init__(message, 403)


class NotFoundException(BusinessException):
    """资源不存在异常"""
    def __init__(self, message: str = "资源不存在"):
        super().__init__(message, 404)


class DuplicateException(BusinessException):
    """数据重复异常"""
    def __init__(self, message: str):
        super().__init__(message, 409)
