from typing import Any, Optional, Union

from .types import Ordering, Op, NullCheck, OrderingNulls


class Expression:
    def __init__(
            self,
            lhs: Any,
            op: Optional[Op] = None,
            rhs: Optional[Any] = None,
            alias: Optional[str] = None,
    ):

        self.lhs: Union["Expression", str] = (
            lhs if isinstance(lhs, Expression) else str(lhs)
        )
        self.negate = False
        self.op = op
        self.rhs = rhs
        self._alias = alias
        self.cast_to: Optional[str] = None
        self.ordering: Optional[Ordering] = None
        self.null_check: Optional[NullCheck] = None
        self.ordering_nulls: Optional[OrderingNulls] = None

    def cast(self, t: str) -> "Expression":
        self.cast_to = t
        return self

    def alias(self, a: str) -> "Expression":
        self._alias = a
        return self

    def is_not_null(self) -> "Expression":
        self.null_check = NullCheck.IS_NOT_NULL
        return self

    def is_null(self) -> "Expression":
        self.null_check = NullCheck.IS_NULL
        return self

    # Using any operator functions will set alias to None in the resulting function; otherwise
    # Something as SomeAlias + SomethingElse as SomeOtherAlias
    # is possible.
    def __reset_aliases(self):
        """Reset aliases for lhs and rhs if they are Expression instances."""
        if isinstance(self.lhs, Expression):
            self.lhs._alias = None
        if isinstance(self.rhs, Expression):
            self.rhs._alias = None

    def __invert__(self) -> "Expression":
        """
        Negates the expression using the NOT operator.
        """

        self.negate = True
        self.__reset_aliases()
        return self

    def __and__(self, other: Union["Expression", str]) -> "Expression":
        other = other if isinstance(other, Expression) else Expression(other)
        result = Expression(lhs=self, op=Op.AND, rhs=other)
        result.__reset_aliases()
        return result

    def __or__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else Expression(other)
        result = Expression(lhs=self, op=Op.OR, rhs=other)
        result.__reset_aliases()
        return result

    def __lt__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else Expression(other)
        result = Expression(lhs=self, op=Op.LT, rhs=other)
        result.__reset_aliases()
        return result

    def __le__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else Expression(other)
        result = Expression(lhs=self, op=Op.LEQ, rhs=other)
        result.__reset_aliases()
        return result

    def __gt__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else Expression(other)
        result = Expression(lhs=self, op=Op.GT, rhs=other)
        result.__reset_aliases()
        return result

    def __ge__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else Expression(other)
        result = Expression(lhs=self, op=Op.GEQ, rhs=other)
        result.__reset_aliases()
        return result

    def __add__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else Expression(other)
        result = Expression(lhs=self, op=Op.ADD, rhs=other)
        result.__reset_aliases()
        return result

    def __sub__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else Expression(other)
        result = Expression(lhs=self, op=Op.SUB, rhs=other)
        result.__reset_aliases()
        return result

    def __mul__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else Expression(other)
        result = Expression(lhs=self, op=Op.MUL, rhs=other)
        result.__reset_aliases()
        return result

    def __truediv__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else Expression(other)
        result = Expression(lhs=self, op=Op.DIV, rhs=other)
        result.__reset_aliases()
        return result

    def __mod__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else Expression(other)
        result = Expression(lhs=self, op=Op.MOD, rhs=other)
        result.__reset_aliases()
        return result

    def eq(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else Expression(other)
        result = Expression(lhs=self, op=Op.EQ, rhs=other)
        result.__reset_aliases()
        return result

    def neq(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else Expression(other)
        result = Expression(lhs=self, op=Op.NEQ, rhs=other)
        result.__reset_aliases()
        return result

    def desc(self) -> "Expression":
        self.ordering = Ordering.DESC
        return self

    def asc(self) -> "Expression":
        self.ordering = Ordering.ASC
        return self

    def nulls_first(self) -> "Expression":
        self.ordering_nulls = OrderingNulls.NULLS_FIRST
        return self

    def nulls_last(self) -> "Expression":
        self.ordering_nulls = OrderingNulls.NULLS_LAST
        return self

    def between(self, lower: "Expression", upper: "Expression") -> "Expression":
        result = Expression(
            lhs=self,
            op=Op.BETWEEN,
            rhs=Expression(f"{lower.to_string()} and {upper.to_string()}"),
        )
        result.__reset_aliases()
        return result

    def to_string(self) -> str:
        """Render the expression as a SQL-compatible string."""
        # Render lhs
        lhs_str = (
            f"{self.lhs.to_string()}"
            if isinstance(self.lhs, Expression)
            else str(self.lhs)
        )

        # Render rhs if it exists
        rhs_str = (
            f"{self.rhs.to_string()}"
            if self.rhs and isinstance(self.rhs, Expression)
            else str(self.rhs) if self.rhs else ""
        )

        # Build the expression string
        if self.op is None:  # Unary or single-value case
            result = lhs_str
        else:  # Binary operator case
            result = f"({lhs_str} {self.op.value} {rhs_str})"

        # Apply NOT if negate is True
        if self.negate:
            result = f"not {result}"

        # Add casting, if any
        if self.cast_to is not None:
            result += f"::{self.cast_to}"

        # Add alias, if present
        if self._alias:
            result += f" as {self._alias}"

        # Apply null check if it exists
        if self.null_check:
            result += " " + self.null_check.value

        return result

    def __repr__(self) -> str:
        return f"Expression({self.to_string()})"
