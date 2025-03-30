import msgspec

from uuid import UUID

from litestar.dto import MsgspecDTO, DTOConfig


class ListScheme(msgspec.Struct):
    id: UUID
    title: str


class ListCreateScheme(msgspec.Struct):
    title: str


class Note(msgspec.Struct):
    id: UUID
    text: str
    list_id: UUID


class ListReadDTO(MsgspecDTO[ListScheme]):
    config = DTOConfig()
