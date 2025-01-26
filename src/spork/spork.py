from typing import Any, Optional

from .expression import Expression
from .func_expr import FuncExpr
from .types import FuncLabel


def col(c: Any) -> Expression:
    if isinstance(c, Expression):
        # If it's already an Expression, return it directly
        return c

    return Expression(lhs=c)


def lit(value: Any) -> Expression:
    """
    Turns any passed value into a trivial literal expression. A literal is simply an Expression with no operations.
    """
    return Expression(lhs=value)


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
