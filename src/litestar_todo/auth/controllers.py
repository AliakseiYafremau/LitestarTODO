from __future__ import annotations

from litestar import Response, Router
from litestar.controller import Controller
from litestar.di import Provide
from litestar.handlers.http_handlers.decorators import post
from litestar.status_codes import HTTP_400_BAD_REQUEST

from litestar_todo.auth.dto import (
    TokenScheme,
    UserCreateScheme,
)
from litestar_todo.auth.services.auth_service import AuthService, provide_auth_service
from litestar_todo.main.config import settings


class AuthController(Controller):
    """Controller for managing todo notes."""

    def __init__(self, owner: Router) -> None:
        """Initialize the UserController."""
        super().__init__(owner)
        self.path = "/auth"
        self.dependencies = {"auth_service": Provide(provide_auth_service)}

    @post()
    async def authenticate(
        self,
        data: UserCreateScheme,
        auth_service: AuthService,
    ) -> TokenScheme | Response:
        """Endpoint for authenticating a user."""
        result = await auth_service.authenticate(data=data)
        if result is None:
            return Response(
                content={"message": "Invalid credentials"},
                status_code=HTTP_400_BAD_REQUEST,
            )
        token = await auth_service.generate_token(
            user_id=result.id,
            secret=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return TokenScheme(access_token=token, token_type="bearer")
