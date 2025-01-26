class Entity:
    """
    An Entity functions much as an Expression, but represents a table or view.
    """

    def __init__(self, ref: str):
        self.ref = ref
        self._alias = ""

    def alias(self, to: str):
        self._alias = to
        return self

    def to_string(self) -> str:
        return f"{self.ref} {self._alias}"
