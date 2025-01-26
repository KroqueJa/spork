from enum import Enum, unique


@unique
class Op(Enum):
    """
    Enum class describing a logical operation such as `NOT` or `EQ`.

    This enum is used internally, and not intended to be exposed to end users.
    """

    NOT = "~"
    EQ = "=="
    NEQ = "<>"
    LEQ = "<="
    GEQ = ">="
    LT = "<"
    GT = ">"
    BETWEEN = "between"
    AND = "and"
    OR = "or"
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"


@unique
class FuncLabel(Enum):
    ROW_NUMBER = "row_number"
    MAX = "max"
    MIN = "min"
    AVG = "avg"
    RANK = "rank"
    DENSE_RANK = "dense_rank"
    FIRST_VALUE = "first_value"
    LAST_VALUE = "last_value"
    LEAD = "lead"
    LAG = "lag"


@unique
class Ordering(Enum):
    DESC = "desc"
    ASC = "asc"


@unique
class InclusionType(Enum):
    FROM = "from"
    INNER = "inner"
    LEFT = "left"
    RIGHT = "right"
    FULL_OUTER = "full outer"
    LEFT_ANTI = "left anti"
    RIGHT_ANTI = "right anti"
