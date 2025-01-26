from typing import Optional, Union

from .expression import Expression
from .types import Ordering


class RowSpec:
    """
    Represents the bounds for a window's rows, with optional arithmetic for offsets.
    """

    def __init__(self, value: Optional[str] = None, offset: Optional[int] = None):
        self.value = value
        self.offset = offset

    def __sub__(self, other: int) -> "RowSpec":
        if not isinstance(other, int):
            raise ValueError("RowsBetween can only be offset by an integer.")
        return RowSpec(
            value=self.value,
            offset=(-other if self.offset is None else self.offset - other),
        )

    def __add__(self, other: int) -> "RowSpec":
        if not isinstance(other, int):
            raise ValueError("RowsBetween can only be offset by an integer.")
        return RowSpec(
            value=self.value,
            offset=(other if self.offset is None else self.offset + other),
        )

    def to_string(self) -> str:
        """
        Render as SQL-compatible string.
        """
        if self.value == "unbounded preceding":
            return "unbounded preceding"
        elif self.value == "unbounded following":
            return "unbounded following"
        elif self.value == "current row":
            return f"current row {self.offset:+d}" if self.offset else "current row"
        else:
            raise ValueError(f"Unsupported RowsBetween value: {self.value}")

    def __repr__(self) -> str:
        return f"RowsBetween(value={self.value}, offset={self.offset})"


def unbounded_preceding() -> RowSpec:
    return RowSpec(value="unbounded preceding")


def unbounded_following() -> RowSpec:
    return RowSpec(value="unbounded following")


def current_row() -> RowSpec:
    return RowSpec(value="current row")


class Window:
    def __init__(
        self,
        partitionby: Optional[Union[str, Expression]] = None,
        orderby: Optional[Union[str, Expression]] = None,
        ordering: Optional[Ordering] = None,
        rowsbetween_lhs: Optional[RowSpec] = None,
        rowsbetween_rhs: Optional[RowSpec] = None,
    ):
        self.partitionby = partitionby
        self.orderby = orderby
        self.ordering = ordering
        self.rowsbetween_lhs = rowsbetween_lhs or unbounded_preceding()
        self.rowsbetween_rhs = rowsbetween_rhs or current_row()

    def rows_between(self, lb: RowSpec, ub: RowSpec) -> "Window":
        # Validate that the lower bound precedes or is equal to the upper bound
        valid_order = (
            (lb.value == "unbounded preceding")
            or (ub.value == "unbounded following")
            or lb.value == "current row"
            and ub.value == "current row"
        )
        if not valid_order:
            raise ValueError(
                f"Invalid bounds: rows between {lb.to_string()} and {ub.to_string()}"
            )
        self.rowsbetween_lhs = lb
        self.rowsbetween_rhs = ub
        return self

    def to_string(self) -> str:
        """
        Render the window specification as a SQL-compatible string.
        """
        parts = []

        # Handle partition by
        if self.partitionby:
            partitionby_str = (
                self.partitionby.to_string()
                if isinstance(self.partitionby, Expression)
                else str(self.partitionby)
            )
            parts.append(f"partition by {partitionby_str}")

        # Handle order by
        if self.orderby:
            orderby_str = (
                self.orderby.to_string()
                if isinstance(self.orderby, Expression)
                else str(self.orderby)
            )
            order_clause = f"order by {orderby_str}"
            if self.ordering:
                order_clause += f" {self.ordering.value}"
            parts.append(order_clause)

        # Handle rows between
        if self.rowsbetween_lhs or self.rowsbetween_rhs:
            rows_clause = (
                f"rows between {self.rowsbetween_lhs.to_string()} "
                f"and {self.rowsbetween_rhs.to_string()}"
            )
            parts.append(rows_clause)

        return f"({' '.join(parts)})"

    def partition_by(self, s: Union[str, Expression]) -> "Window":
        self.partitionby = s
        return self

    def order_by(
        self, orderby: Union[str, Expression], ordering: Optional[Ordering] = None
    ) -> "Window":
        self.orderby = orderby
        self.ordering = ordering
        return self

    def desc(self) -> "Window":
        self.ordering = Ordering.DESC
        return self

    def asc(self) -> "Window":
        self.ordering = Ordering.ASC
        return self
