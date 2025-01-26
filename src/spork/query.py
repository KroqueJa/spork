from typing import Union, Optional, List

from spork.types import InclusionType, OrderingNulls
from spork.expression import Expression
from spork.entity import Entity


class Selection:
    """
    The first part of a query.
    """

    def __init__(self, *cols: Union[Expression, str]):
        """
        Accepts a variable number of arguments for columns, which can be
        either strings or Expression objects.
        """
        self.cols = [Expression(col) if isinstance(col, str) else col for col in cols]

    def __add__(self, rhs: "Selection") -> "Selection":
        if not isinstance(rhs, Selection):
            raise ValueError("Can only add another Selection object.")

        # Combine columns and return a new Selection
        combined_cols = self.cols + rhs.cols
        return Selection(*combined_cols)

    def to_string(self) -> str:
        """
        Render the selection as a SQL-compatible string.
        """
        s = "select\n" + ",\n".join([exp.to_string() for exp in self.cols])
        return s


class Join:
    def __init__(
        self,
        what: Union[Entity, Expression, "Query"],
        on: Expression,
        how: Optional[Union[InclusionType, str]] = None,
    ):
        self.what = what
        self.on = on

        if how:
            if isinstance(how, str):
                try:
                    # Convert string to enum (case-insensitive)
                    how = InclusionType[how.upper().replace(" ", "_")]
                except KeyError:
                    raise ValueError(f"Invalid join type: {how}")

        self.how = how if how else InclusionType.INNER

    def to_string(self) -> str:
        return f"{self.how.value} join {self.what.to_string()} on {self.on.to_string()}"


class Dataset:
    """
    A list of included entities - one Entity and some joins
    """

    def __init__(self, entity: Entity, *joins: Join):
        self.entity = entity
        self.joins = [e for e in joins]
        self._alias = ""

    def alias(self, _alias: str) -> "Dataset":
        self._alias = _alias
        return self

    def join(
        self,
        what: Union[Entity, Expression, "Query"],
        on: Expression,
        how: Optional[Union[InclusionType, str]] = None,
    ) -> "Dataset":
        self.joins.append(Join(what, on, how))
        return self

    def to_string(self) -> str:
        joins = "\n".join([j.to_string() for j in self.joins])
        s = f"from {self.entity.to_string()}\n{joins}"
        return s


class Query:
    """
    Represents a SQL query with select, from, and optional where, group by, order by, having, and qualify clauses.
    """

    def __init__(
        self, selection: Optional[Selection] = None, dataset: Optional[Dataset] = None
    ):
        self.selection: Optional[Selection] = selection
        self.dataset: Optional[Dataset] = dataset
        self._where: Optional[Expression] = None
        self._group_by: Optional[List[Expression]] = None
        self._order_by: Optional[List[Expression]] = None
        self._having: Optional[Expression] = None
        self._qualify: Optional[Expression] = None

    def select(self, selection: Selection) -> "Query":
        """
        Set the selection for the query.
        """
        self.selection = selection
        return self

    def fromm(self, dataset: Dataset) -> "Query":
        """
        Set the dataset (from clause) for the query.
        """
        self.dataset = dataset
        return self

    def where(self, exp: Expression) -> "Query":
        """
        Add a where clause to the query.
        """
        self._where = exp
        return self

    def group_by(self, *expressions: Union[Expression, str]) -> "Query":
        """
        Add a group by clause to the query.
        """

        self._group_by = [Expression(exp) for exp in expressions]
        return self

    def order_by(self, *expressions: Union[Expression, str]) -> "Query":
        """
        Add an order by clause to the query.
        """
        self._order_by = [Expression(exp) for exp in expressions]
        return self

    def having(self, exp: Expression) -> "Query":
        """
        Add a having clause to the query.
        """
        self._having = exp
        return self

    def qualify(self, exp: Expression) -> "Query":
        """
        Add a qualify clause to the query.
        """
        self._qualify = exp
        return self

    def to_string(self) -> str:
        """
        Render the query as a SQL-compatible string.
        """
        if not self.selection:
            raise ValueError("A query must have a selection.")
        if not self.dataset:
            raise ValueError("A query must have a dataset.")

        query = self.selection.to_string()
        query += f"\n{self.dataset.to_string()}"

        if self._where:
            query += f"\nwhere {self._where.to_string()}"

        if self._group_by:
            group_by_str = ", ".join([exp.to_string() for exp in self._group_by])
            query += f"\ngroup by {group_by_str}"

        if self._having:
            query += f"\nhaving {self._having.to_string()}"

        if self._order_by:
            order_by_str = ", ".join(
                [
                    f"{exp.to_string()} {exp.ordering.value}"
                    if exp.ordering is not None
                    else f"{exp.to_string()}"
                    for exp in self._order_by
                ]
            )
            query += f"\norder by {order_by_str}"

        if self._qualify:
            query += f"\nqualify {self._qualify.to_string()}"

        return query
