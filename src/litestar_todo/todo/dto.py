from uuid import UUID

import msgspec


class NoteScheme(msgspec.Struct):
    """Note class.

    Attributes:
        id (UUID): The ID of the note.
        text (str): The text of the note.

    """

    id: UUID
    text: str


class NoteCreateScheme(msgspec.Struct):
    """Scheme for creating a new note.

    Attributes:
        text (str): The text of the note.

    """

    text: str


class NoteReadScheme(msgspec.Struct):
    """NoteReadScheme class.

    Attributes:
        id (UUID): The ID of the note.
        text (str): The text of the note.

    """

    id: UUID
    text: str
