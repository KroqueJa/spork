from typing import Any, Optional

from .expression import Expression, Literal
from .func_expr import FuncExpr
from .types import FuncLabel


def col(c: Any) -> Expression:
    if isinstance(c, Expression):
        # If it's already an Expression, return it directly
        return c

    return Expression(lhs=c)


def lit(value: Any) -> Literal:
    """
    Turns any passed value into a trivial literal expression.
    If the value is already a Literal, it is returned as-is.
    """
    if isinstance(value, Literal):
        return value
    if isinstance(value, Expression):
        raise ValueError(
            "ERROR | This function should not be used on expressions; did you mean to use `Col`?"
        )

    return Literal(value)


def row_number() -> FuncExpr:
    return FuncExpr(f=FuncLabel.ROW_NUMBER)


def lag(
    column: str, rows: Optional[int] = None, default_value: Optional[str] = None
) -> FuncExpr:
    """
    Create a LAG function expression.
    """
    args = [col(column)]
    if rows is not None:
        args.append(rows)
    if default_value is not None:
        args.append(lit(default_value))
    return FuncExpr(f=FuncLabel.LAG, args=args)
