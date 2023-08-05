"""Collection of objects returned by the different loaders."""

# Standard library
from enum import (
    Enum,
)
from typing import (
    Any,
    NamedTuple,
)


class Type(Enum):
    """Enumeration for all possible `Node` data types."""
    ARRAY: str = 'ARRAY'
    """Indicates an array data-type: Example: `[]`"""
    BOOLEAN: str = 'BOOLEAN'
    """Indicates a boolean data-type: Example: `true`"""
    BINARY: str = 'BINARY'
    """Indicates a binary data-type: Example: b'true'"""
    DATETIME: str = 'DATETIME'
    """Indicates a datetime data-type: Example: datetime(2020, 12, 31)"""
    NUMBER: str = 'NUMBER'
    """Indicates a numeric data-type: Example: `123.4`"""
    NULL: str = 'NULL'
    """Indicates a null data-type: Example: `null`"""
    OBJECT: str = 'OBJECT'
    """Indicates an object data-type: Example: `{}`"""
    STRING: str = 'STRING'
    """Indicates a string data-type: Example: `"example"`"""


class Node(NamedTuple):
    """Represents any JSON token and its metadata."""
    data: Any
    """Contains the raw inner element data."""
    data_type: Type
    """Defines the inner element type."""
    end_column: int
    """End column for the element."""
    end_line: int
    """End line for the element."""
    start_column: int
    """Start column for the element."""
    start_line: int
    """Start line for the element."""

    @property
    def inner(self) -> Any:
        """Access the wrapped data by this `Node`.

        The access method follow some rules:

        - Arrays are simplified 1 level: [a, b] -> [a.data, b.data]
        - Objects are simplified on its keys only: {a: b} -> {a.data: b}
        - Everything else returns the inner data as per `Node.data`
        """
        data: Any
        if self.data_type is Type.ARRAY:
            data = [val.data for val in self.data]
        elif self.data_type is Type.OBJECT:
            data = {key.data: val for key, val in self.data.items()}
        else:
            data = self.data

        return data

    @property
    def raw(self) -> Any:
        """Access the wrapped data by this `Node`, recursing into sub-objects.
        """
        data: Any
        if self.data_type is Type.ARRAY:
            data = [val.raw for val in self.data]
        elif self.data_type is Type.OBJECT:
            data = {key.raw: val.raw for key, val in self.data.items()}
        else:
            data = self.data

        return data

    def __repr__(self) -> str:
        return f"""Node(
            data={self.data},
            data_type={self.data_type},
            end_column={self.end_column},
            end_line={self.end_line},
            start_column={self.start_column},
            start_line={self.start_line},
        )"""
