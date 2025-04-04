from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Vec2:
    x: int
    y: int

    @classmethod
    def left(cls):
        return cls(-1, 0)

    @classmethod
    def right(cls):
        return cls(1, 0)

    @classmethod
    def up(cls):
        return cls(0, -1)

    @classmethod
    def down(cls):
        return cls(0, 1)

    @property
    def _tuple(self):
        return self.x, self.y

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __add__(self, other: Vec2):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2):
        return self + -other

    def __mul__(self, other: int):
        return Vec2(self.x * other, self.y * other)

    def __eq__(self, other: object):
        return isinstance(other, Vec2) and self._tuple == other._tuple

    def __hash__(self):
        return hash(self._tuple)
