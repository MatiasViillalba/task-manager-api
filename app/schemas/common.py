from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic schema for paginated API responses.

    Attributes:
        total: Total number of items available.
        limit: Maximum number of items returned in this response.
        offset: Number of items skipped before this response.
        items: List of items for the current page.
    """

    total: int
    limit: int
    offset: int
    items: list[T]
