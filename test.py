from functools import wraps

from fastapi import Request

from app.core.exceptions.custom_exception import UnauthorizedException
from app.enums.user_role import UserRole


def require_role(allowed_roles: list[UserRole]):
    """
    특정 role만 접근 가능하도록 하는 데코레이터

    사용 예시:
    @require_role([UserRole.SYSTEM_ADMIN])
    def get_zaixun(request: Request):
        ...

    @require_role([UserRole.SYSTEM_ADMIN, UserRole.GITHUB_USER])
    def delete_zaixun(request: Request):
        ...
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            # jwt_middleware.py에서 request.state에 저장한 UserRole enum 가져오기
            current_role = getattr(request.state, "current_role", None)

            if not current_role:
                raise UnauthorizedException()

            if current_role not in allowed_roles:
                raise UnauthorizedException()

            return func(request, *args, **kwargs)

        return wrapper

    return decorator
