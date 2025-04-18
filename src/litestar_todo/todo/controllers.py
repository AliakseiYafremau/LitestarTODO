from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from litestar import Response, Router
from litestar.controller import Controller
from litestar.di import Provide
from litestar.handlers.http_handlers.decorators import delete, get, post
from litestar.status_codes import HTTP_400_BAD_REQUEST

from litestar_todo.auth.services.auth_service import login_required
from litestar_todo.todo.dto import (
    NoteReadScheme,
)
from litestar_todo.todo.servicies import (
    NoteService,
    provide_note_service,
)

if TYPE_CHECKING:
    from uuid import UUID

    from litestar_todo.todo.dto import (
        NoteReadScheme,
    )


class NoteController(Controller):
    """Controller for managing todo notes."""

    def __init__(self, owner: Router) -> None:
        """Initialize the NoteController."""
        super().__init__(owner)
        self.path = "/note"
        self.dependencies = {"note_service": Provide(provide_note_service)}

    @get()
    async def get_note(
        self,
        note_id: UUID,
        note_service: NoteService,
    ) -> NoteReadScheme | Response:
        """Endpoint for retrieving a single todo note."""
        result = await note_service.get_by_id(note_id=note_id)
        if result is None:
            return Response(
                content={"message": "Invalid input"},
                status_code=HTTP_400_BAD_REQUEST,
            )
        return result

    @login_required
    @get("/all")
    async def get_all(self, note_service: NoteService) -> list[NoteReadScheme]:
        """Endpoint for retrieving all todo notes."""
        return await note_service.get_all()

    @post()
    async def create_note(
        self,
        data: NoteReadScheme,
        note_service: NoteService,
    ) -> NoteReadScheme | Response:
        """Endpoint for creating a new todo note."""
        result = await note_service.create(text=data.text)
        if result is None:
            return Response(
                content={"message": "Invalid input"},
                status_code=HTTP_400_BAD_REQUEST,
            )
        return result

    @delete("/{note_id:uuid}")
    async def delete_note(self, note_id: UUID, note_service: NoteService) -> None:
        """Endpoint for deleting a todo note."""
        await note_service.delete(note_id=note_id)
