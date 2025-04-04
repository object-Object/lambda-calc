from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from string import ascii_lowercase


class BaseExpression(ABC):
    pass


@dataclass
class Abstraction(BaseExpression):
    body: Expression


@dataclass
class Application(BaseExpression):
    function: Expression
    argument: Expression


@dataclass
class Variable(BaseExpression):
    index: int


type Expression = Abstraction | Application | Variable


def display_with_names(
    expression: Expression,
    names: str = ascii_lowercase,
    depth: int = 0,
) -> str:
    match expression:
        case Abstraction():
            name = names[depth]
            body = display_with_names(expression.body, names, depth + 1)
            return f"(λ{name}.{body})"
        case Application():
            function = display_with_names(expression.function, names, depth)
            argument = display_with_names(expression.argument, names, depth)
            return f"({function}{argument})"
        case Variable():
            return names[depth - expression.index]
