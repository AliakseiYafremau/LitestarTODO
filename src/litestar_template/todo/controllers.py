from litestar.controller import Controller
from litestar.handlers.http_handlers.decorators import get, post
from litestar.di import Provide

from litestar_template.todo.dto import ListReadDTO
from litestar_template.todo.servicies import provide_list_service, ListService

class ListController(Controller):
    dependencies = {"list_service": Provide(provide_list_service)}

    @get("/list")
    async def list_list(self, list_id: int, list_service: ListService) -> list[ListReadDTO]:
        return list_service.get_by_id(list_id=list_id)
