from typing import ClassVar
from uuid import UUID

from litestar.controller import Controller
from litestar.di import Provide
from litestar.handlers.http_handlers.decorators import delete, get, post

from litestar_todo.todo.dto import ListCreateScheme, ListReadDTO
from litestar_todo.todo.servicies import ListService, provide_list_service


class ListController(Controller):
    """Controller for managing todo lists."""

    path: ClassVar[str] = "/list"
    dependencies: ClassVar[dict[str, Provide]] = {
        "list_service": Provide(provide_list_service)
    }

    @get()
    async def list_list(
        self, list_id: UUID, list_service: ListService
    ) -> list[ListReadDTO]:
        """Endpoint for retrieving a single todo list."""
        return await list_service.get_by_id(list_id=list_id)

    @get("/all")
    async def list_lists(self, list_service: ListService) -> list[ListReadDTO]:
        """Endpoint for retrieving all todo lists."""
        return await list_service.get_all()

    @post()
    async def create_list(
        self, data: ListCreateScheme, list_service: ListService
    ) -> ListReadDTO:
        """Endpoint for creating a new todo list."""
        return await list_service.create(title=data.title)

    @delete("/{list_id:uuid}")
    async def delete_list(self, list_id: UUID, list_service: ListService) -> None:
        """Endpoint for deleting a todo list."""
        await list_service.delete(list_id=list_id)
