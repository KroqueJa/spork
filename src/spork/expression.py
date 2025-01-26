from typing import Any, Optional, Union

from .types import Ordering, Op


class Expression:
    def __init__(
        self,
        lhs: Any,
        op: Optional[Op] = None,
        rhs: Optional["Expression"] = None,
        alias: Optional[str] = None,
    ):
        self.lhs: Union["Expression", str] = (
            lhs if isinstance(lhs, Expression) else str(lhs)
        )
        self.op = op
        self.rhs = rhs
        self._alias = alias
        self.cast_to: Optional[str] = None
        self.ordering: Optional[Ordering] = None

    def cast(self, t: str) -> "Expression":
        self.cast_to = t
        return self

    def alias(self, a: str) -> "Expression":
        self._alias = a
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
        if self.op is None:
            raise ValueError("Cannot apply NOT (~) to an incomplete expression.")

        # Create a NOT expression with the current expression as the lhs
        result = Expression(lhs=self, op=Op.NOT)
        result.__reset_aliases()
        return result

    def __and__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else lit(other)
        result = Expression(lhs=self, op=Op.AND, rhs=other)
        result.__reset_aliases()
        return result

    def __or__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else lit(other)
        result = Expression(lhs=self, op=Op.OR, rhs=other)
        result.__reset_aliases()
        return result

    def __lt__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else lit(other)
        result = Expression(lhs=self, op=Op.LT, rhs=other)
        result.__reset_aliases()
        return result

    def __le__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else lit(other)
        result = Expression(lhs=self, op=Op.LEQ, rhs=other)
        result.__reset_aliases()
        return result

    def __gt__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else lit(other)
        result = Expression(lhs=self, op=Op.GT, rhs=other)
        result.__reset_aliases()
        return result

    def __ge__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else lit(other)
        result = Expression(lhs=self, op=Op.GEQ, rhs=other)
        result.__reset_aliases()
        return result

    def __add__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else lit(other)
        result = Expression(lhs=self, op=Op.ADD, rhs=other)
        result.__reset_aliases()
        return result

    def __sub__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else lit(other)
        result = Expression(lhs=self, op=Op.SUB, rhs=other)
        result.__reset_aliases()
        return result

    def __mul__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else lit(other)
        result = Expression(lhs=self, op=Op.MUL, rhs=other)
        result.__reset_aliases()
        return result

    def __truediv__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else lit(other)
        result = Expression(lhs=self, op=Op.DIV, rhs=other)
        result.__reset_aliases()
        return result

    def __mod__(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else lit(other)
        result = Expression(lhs=self, op=Op.MOD, rhs=other)
        result.__reset_aliases()
        return result

    def eq(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else lit(other)
        result = Expression(lhs=self, op=Op.EQ, rhs=other)
        result.__reset_aliases()
        return result

    def neq(self, other: "Expression") -> "Expression":
        other = other if isinstance(other, Expression) else lit(other)
        result = Expression(lhs=self, op=Op.NEQ, rhs=other)
        result.__reset_aliases()
        return result

    def desc(self) -> "Expression":
        self.ordering = Ordering.DESC
        return self

    def asc(self) -> "Expression":
        self.ordering = Ordering.ASC
        return self

    def between(self, lower: "Expression", upper: "Expression") -> "Expression":
        result = Expression(
            lhs=self,
            op=Op.BETWEEN,
            rhs=col(f"{lower.to_string()} and {upper.to_string()}"),
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

        # Handle NOT operator specifically
        if self.op == Op.NOT:
            return f"NOT ({lhs_str})"  # Use SQL keyword NOT

        # Handle cases with no operator
        if self.op is None:
            if self.cast_to is not None:
                lhs_str += f"::{self.cast_to}"
            if self._alias:
                lhs_str += f" as {self._alias}"
            return lhs_str

        # Render rhs
        rhs_str = (
            f"{self.rhs.to_string()}"
            if isinstance(self.rhs, Expression)
            else str(self.rhs)
        )

        # Construct the full expression
        s = f"({lhs_str} {self.op.value} {rhs_str})"

        # Add casting, if any
        if self.cast_to is not None:
            s += f"::{self.cast_to}"

        # Add alias, if present
        if self._alias:
            s += f" as {self._alias}"

        return s

    def __repr__(self) -> str:
        return f"Expression({self.to_string()})"


class Literal(Expression):
    """
    Wraps a literal in a context-sensitive way, so that e.g. strings are represented with single quotes,
    numbers are left as-is, and None translates to NULL for SQL purposes.
    """

    def __init__(self, value: Any):
        self.value = value
        self.cast_to = None

    def cast(self, t: str) -> "Expression":
        self.cast_to = t
        return self

    def to_string(self) -> str:
        """
        Render the literal as a SQL-compatible string.
        """
        s = ""
        if self.value is None:
            s = "NULL"
        elif isinstance(self.value, str):
            replaced = self.value.replace("'", "''")
            s = f"'{replaced}'"
        elif isinstance(self.value, bool):
            s = "TRUE" if self.value else "FALSE"
        elif isinstance(self.value, (int, float)):
            s = str(self.value)
        else:
            raise ValueError(f"ERROR | Unsupported literal type: {type(self.value)}")

        if self.cast_to is not None:
            s += f"::{self.cast_to}"

        return s

    def __repr__(self) -> str:
        return f"Literal({self.to_string()})"
