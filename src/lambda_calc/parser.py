from __future__ import annotations

from dataclasses import dataclass, field

from lambda_calc.ast import Abstraction, Application, Expression, Variable
from lambda_calc.diagram import LambdaDiagram
from lambda_calc.math import Vec2


@dataclass
class DiagramWalk:
    pixels: set[Vec2]
    abstractions: set[Vec2]
    applications: set[Vec2]
    min_x: int
    min_y: int
    max_x: int
    max_y: int

    def __contains__(self, pos: Vec2):
        return pos in self.pixels


@dataclass(kw_only=True, eq=False)
class AbstractionToken:
    min_x: int
    max_x: int
    y: int
    scope_max_y: int


@dataclass(kw_only=True, eq=False)
class ApplicationToken:
    min_x: int
    max_x: int
    y: int
    left: Token
    right: Token = field(init=False)


@dataclass(eq=False)
class VariableToken:
    index: int


type Token = AbstractionToken | ApplicationToken | VariableToken


def parse_diagram(diagram: LambdaDiagram):
    walk = _walk_diagram(diagram)
    tokens = _tokenize_diagram(walk)
    return _parse_area(
        tokens,
        min_x=walk.min_x,
        max_x=walk.max_x,
        min_y=walk.min_y,
        max_y=walk.max_y,
    )


def _walk_diagram(diagram: LambdaDiagram):
    queue = [Vec2(0, 0)]

    walk = DiagramWalk(
        pixels=set(queue),
        abstractions=set(),
        applications=set(),
        min_x=0,
        min_y=0,
        max_x=0,
        max_y=0,
    )

    assert diagram[queue[0]]

    while queue:
        pos = queue.pop(0)

        walk.min_x = min(walk.min_x, pos.x)
        walk.min_y = min(walk.min_y, pos.y)
        walk.max_x = max(walk.max_x, pos.x)
        walk.max_y = max(walk.max_y, pos.y)

        adjacents = list[Vec2]()
        if left := diagram[adjacent := pos + Vec2.left()]:
            adjacents.append(adjacent)
        if right := diagram[adjacent := pos + Vec2.right()]:
            adjacents.append(adjacent)
        if up := diagram[adjacent := pos + Vec2.up()]:
            adjacents.append(adjacent)
        if down := diagram[adjacent := pos + Vec2.down()]:
            adjacents.append(adjacent)

        if right and not left and not up and not down:
            walk.abstractions.add(pos)

            # only check two up/down if it's the start of an abstraction
            if diagram[adjacent := pos + Vec2.up() * 2]:
                adjacents.append(adjacent)
            if diagram[adjacent := pos + Vec2.down() * 2]:
                adjacents.append(adjacent)

        elif up and right and not left:
            walk.applications.add(pos)

        for adjacent in adjacents:
            if adjacent not in walk.pixels:
                walk.pixels.add(adjacent)
                queue.append(adjacent)

    return walk


def _tokenize_diagram(walk: DiagramWalk):
    tokens = dict[Vec2, Token]()
    abstractions = list[AbstractionToken]()

    for abstraction_pos in sorted(walk.abstractions, key=lambda v: v.y):
        abstraction = AbstractionToken(
            min_x=abstraction_pos.x,
            max_x=abstraction_pos.x,
            y=abstraction_pos.y,
            scope_max_y=abstraction_pos.y,
        )
        abstractions.append(abstraction)

        while abstraction_pos in walk:
            if abstraction_pos + Vec2.up() not in walk:
                variable_pos = abstraction_pos + Vec2.down()
                variable = VariableToken(1)
                while variable_pos in walk:
                    left = variable_pos + Vec2.left() in walk
                    right = variable_pos + Vec2.right() in walk
                    match left, right:
                        case False, False:
                            # same chunk of variable
                            tokens[variable_pos] = variable
                        case True, True:
                            # nested abstraction
                            variable = VariableToken(variable.index + 1)
                        case _:
                            # application
                            break
                    variable_pos += Vec2.down()

            abstraction.max_x = abstraction_pos.x
            tokens[abstraction_pos] = abstraction
            abstraction_pos += Vec2.right()

    for application_pos in sorted(walk.applications, key=lambda v: v.y):
        application = ApplicationToken(
            min_x=application_pos.x,
            max_x=application_pos.x,
            y=application_pos.y,
            left=tokens[application_pos + Vec2.up()],
        )

        while application_pos in walk:
            tail_pos = application_pos + Vec2.down()
            while tail_pos in walk:
                if tail_pos + Vec2.left() in walk or tail_pos + Vec2.right() in walk:
                    # reached another application
                    break
                tokens[tail_pos] = application
                tail_pos += Vec2.down()

            application.max_x = application_pos.x
            tokens[application_pos] = application
            application_pos += Vec2.right()

        application.right = tokens[Vec2(application.max_x, application.y) + Vec2.up()]

    # find the first application that leaves each abstraction's scope
    for abstraction in abstractions:
        for y in range(abstraction.y, walk.max_y + 1):
            if isinstance(
                token := tokens.get(Vec2(abstraction.min_x, y)), ApplicationToken
            ):
                if not isinstance(token.right, AbstractionToken):
                    token.right = abstraction
                break

            if isinstance(
                token := tokens.get(Vec2(abstraction.max_x, y)), ApplicationToken
            ):
                if not isinstance(token.left, AbstractionToken):
                    token.left = abstraction
                break

            abstraction.scope_max_y = y

    return tokens


def _parse_area(
    tokens: dict[Vec2, Token],
    *,
    min_x: int,
    max_x: int,
    min_y: int,
    max_y: int,
) -> Expression:
    # check how many tokens are on this row
    result: Token | None = None
    for x in range(min_x, max_x + 1):
        if token := tokens.get(Vec2(x, min_y)):
            if result is None:
                result = token
            elif result is not token:
                break
    else:
        # if we didn't break, there's only one token on this row
        # which means that's the value of this area
        if result is None:
            raise ValueError(
                f"Expected to find at least one token, but none were found: x=[{min_x}, {max_x}], y={min_y}"
            )
        return _parse_token(tokens, result)

    # otherwise, the result is an application at the bottom of the area
    for x in range(min_x, max_x + 1):
        match tokens.get(Vec2(x, max_y)):
            case ApplicationToken() as application:
                return _parse_token(tokens, application)
            case None:
                pass
            case token:
                raise ValueError(
                    f"Expected an application, but got {token}: x=[{min_x}, {max_x}], y={max_y}"
                )

    raise ValueError(
        f"Expected to find at least one token, but none were found: x=[{min_x}, {max_x}], y={max_y}"
    )


def _parse_token(tokens: dict[Vec2, Token], token: Token) -> Expression:
    match token:
        case AbstractionToken():
            return Abstraction(
                body=_parse_area(
                    tokens,
                    min_x=token.min_x,
                    max_x=token.max_x,
                    min_y=token.y + 2,
                    max_y=token.scope_max_y,
                )
            )
        case ApplicationToken():
            return Application(
                function=_parse_token(tokens, token.left),
                argument=_parse_token(tokens, token.right),
            )
        case VariableToken():
            return Variable(index=token.index)
