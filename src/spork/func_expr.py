from typing import Optional, Union, List

from spork.expression import Expression
from spork.types import FuncLabel
from spork.window import Window


class FuncExpr(Expression):
    """
    Subclass of Expression representing functions with optional window clauses.
    Example: row_number() over (partition by thing order by other_thing desc)
    """

    def __init__(
        self,
        f: FuncLabel,
        args: Optional[List[Union[str, Expression]]] = None,
        window: Optional[Window] = None,
        alias: Optional[str] = None,
    ):
        super().__init__(lhs=f, op=None, rhs=None, alias=alias)
        self.f = f
        self.args = args or []
        self.window = window

    def over(self, window: Window):
        self.window = window
        return self

    def to_string(self) -> str:
        """Render the function as a SQL-compatible string."""
        # Render the function name
        func_str = f"{self.f.value}()"

        # Render arguments if present
        if self.args:
            args_str = ", ".join(
                arg.to_string() if isinstance(arg, Expression) else str(arg)
                for arg in self.args
                if arg is not None  # Skip None values
            )
            func_str = f"{self.f.value}({args_str})"

        # Append window specification if present
        if self.window:
            func_str += f" over {self.window.to_string()}"

        # Add alias if present
        if self._alias:
            func_str += f" as {self._alias}"

        return func_str

    def __repr__(self) -> str:
        return f"FuncExp({self.to_string()})"
