from __future__ import annotations

from typing import TYPE_CHECKING

from litestar import Response
from litestar.controller import Controller
from litestar.di import Provide
from litestar.handlers.http_handlers.decorators import post
from litestar.status_codes import HTTP_400_BAD_REQUEST

from litestar_todo.auth.dto import UserCreateScheme
from litestar_todo.auth.services import AuthService, provide_auth_service
from litestar_todo.auth.utils import jwt_auth

if TYPE_CHECKING:
    from litestar import Router

    from litestar_todo.auth.dto import (
        UserCreateScheme,
    )


class AuthController(Controller):
    """Controller for managing todo notes."""

    def __init__(self, owner: Router) -> None:
        """Initialize the UserController."""
        super().__init__(owner)
        self.path = "/auth"
        self.dependencies = {"auth_service": Provide(provide_auth_service)}

    @post("/login")
    async def login_handler(
        self, auth_service: AuthService, data: UserCreateScheme,
    ) -> Response:
        """Login handler for user authentication.

        Args:
            auth_service: The authentication service used for user operations.
            data: The user credentials.

        Returns:
            A response containing the authenticated user.

        """
        user = await auth_service.get_user_by_username(
            username=data.username,
        )
        if not user:
            return Response(
                content={"message": "Invalid input"},
                status_code=HTTP_400_BAD_REQUEST,
            )
        return jwt_auth.login(identifier=str(user.id))
