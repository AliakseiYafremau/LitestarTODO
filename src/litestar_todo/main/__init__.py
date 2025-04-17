from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from litestar import Response, Router
from litestar.controller import Controller
from litestar.di import Provide
from litestar.handlers.http_handlers.decorators import delete, get, post
from litestar.status_codes import HTTP_400_BAD_REQUEST

from litestar_todo.auth.services.auth_service import AuthService, provide_auth_service
from litestar_todo.auth.services.user_service import UserService, provide_user_service


class UserController(Controller):
    """Controller for managing todo notes."""

    def __init__(self, owner: Router) -> None:
        """Initialize the UserController."""
        super().__init__(owner)
        self.path = "/user"
        self.dependencies = {"user_service": Provide(provide_user_service),
                             "auth_service": Provide(provide_auth_service)}
