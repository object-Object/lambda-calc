import textwrap
from typing import Sequence

from lambda_calc.math import Vec2


class LambdaDiagram:
    def __init__(self, data: Sequence[Sequence[bool]]):
        self.data = data

    @classmethod
    def from_str(cls, data: str):
        data = textwrap.dedent(data).lstrip("\n")
        if not data or data[0].isspace():
            raise ValueError("Top left character must not be blank")
        if "\t" in data:
            raise ValueError("Must use spaces, not tabs")
        return cls([[c != " " for c in line] for line in data.splitlines()])

    def __getitem__(self, pos: Vec2 | tuple[int, int]):
        match pos:
            case Vec2(x=x, y=y):
                pass
            case (x, y):
                pass

        if not (0 <= y < len(self.data)):
            return False
        row = self.data[y]
        if not (0 <= x < len(row)):
            return False
        return row[x]

    def __str__(self):
        return "\n".join("".join("#" if v else " " for v in row) for row in self.data)

    def _ipython_display_(self):
        print(str(self))
