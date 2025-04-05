import pytest

from lambda_calc.ast import Abstraction, Application, Expression, Variable
from lambda_calc.diagram import LambdaDiagram
from lambda_calc.parser import parse_diagram


@pytest.mark.parametrize(
    ["diagram_str", "want_ast"],
    [
        # identity
        # λx.x
        (
            """
            ###
             #
             #
            """,
            Abstraction(Variable(1)),
        ),
        # true
        # λx.λy.x
        (
            """
            ###
             #
            ###
             #
             #
            """,
            Abstraction(Abstraction(Variable(2))),
        ),
        # false
        # λx.λy.y
        (
            """
            ###

            ###
             #
             #
            """,
            Abstraction(Abstraction(Variable(1))),
        ),
        # S
        # λx.λy.λz.(x z)(y z)
        (
            """
            ###############
             #
            ###############
             #       #
            ###############
             #   #   #   #
             #####   #####
             #       #
             #########
             #
             #
            """,
            Abstraction(
                Abstraction(
                    Abstraction(
                        Application(
                            Application(Variable(3), Variable(1)),
                            Application(Variable(2), Variable(1)),
                        )
                    )
                )
            ),
        ),
        (
            """
            ###############
             #
            ###############
             #       #
            ###############
             #   #   #   #
             #####   #####
                 #   #
                 #####
            """,
            Abstraction(
                Abstraction(
                    Abstraction(
                        Application(
                            Application(Variable(3), Variable(1)),
                            Application(Variable(2), Variable(1)),
                        )
                    )
                )
            ),
        ),
        # Y
        # λf.(λx.x x)(λx.f(x x))
        (
            """
            ###################
                     #
            ####### ###########
             #   #   #   #   #
             #####   #   #####
             #       #   #
             #       #####
             #       #
             #########
             #
             #
            """,
            Abstraction(
                Application(
                    Abstraction(Application(Variable(1), Variable(1))),
                    Abstraction(
                        Application(
                            Variable(2),
                            Application(Variable(1), Variable(1)),
                        )
                    ),
                )
            ),
        ),
        (
            """
            ###################
                     #
            ####### ###########
             #   #   #   #   #
             #####   #   #####
                 #   #   #
                 #   #####
                 #   #
                 #####
            """,
            Abstraction(
                Application(
                    Abstraction(Application(Variable(1), Variable(1))),
                    Abstraction(
                        Application(
                            Variable(2),
                            Application(Variable(1), Variable(1)),
                        )
                    ),
                )
            ),
        ),
        # 3
        # λf.λx.f(f(f x))
        (
            """
            ###############
             #   #   #
            ###############
             #   #   #   #
             #   #   #####
             #   #   #
             #   #####
             #   #
             #####
             #
             #
            """,
            Abstraction(
                Abstraction(
                    Application(
                        Variable(2),
                        Application(
                            Variable(2),
                            Application(Variable(2), Variable(1)),
                        ),
                    )
                )
            ),
        ),
        (
            """
            ###############
             #   #   #
            ###############
             #   #   #   #
             #   #   #####
             #   #   #
             #   #####
             #   #
             #####
            """,
            Abstraction(
                Abstraction(
                    Application(
                        Variable(2),
                        Application(
                            Variable(2),
                            Application(Variable(2), Variable(1)),
                        ),
                    )
                )
            ),
        ),
        # predecessor
        # λn.λf.λx.n(λg.λh.h(g f))(λu.x)(λu.u)
        (
            """
            #######################
             #
            #######################
             #           #
            #######################
             #           #   #
             #  ########### ### ###
             #       #   #   #   #
             #  ###########  #   #
             #   #   #   #   #   #
             #   #   #####   #   #
             #   #   #       #   #
             #   #####       #   #
             #   #           #   #
             #####           #   #
             #               #   #
             #################   #
             #                   #
             #####################
             #
             #
            """,
            Abstraction(
                Abstraction(
                    Abstraction(
                        Application(
                            Application(
                                Application(
                                    Variable(3),
                                    Abstraction(
                                        Abstraction(
                                            Application(
                                                Variable(1),
                                                Application(Variable(2), Variable(4)),
                                            )
                                        )
                                    ),
                                ),
                                Abstraction(Variable(2)),
                            ),
                            Abstraction(Variable(1)),
                        )
                    )
                )
            ),
        ),
        (
            """
            #######################
             #
            #######################
             #           #
            #######################
             #           #   #
             #  ########### ### ###
             #       #   #   #   #
             #  ###########  #   #
             #   #   #   #   #   #
             #   #   #####   #   #
             #   #   #       #   #
             #   #####       #   #
             #   #           #   #
             #####           #   #
                 #           #   #
                 #############   #
                             #   #
                             #####
            """,
            Abstraction(
                Abstraction(
                    Abstraction(
                        Application(
                            Application(
                                Application(
                                    Variable(3),
                                    Abstraction(
                                        Abstraction(
                                            Application(
                                                Variable(1),
                                                Application(Variable(2), Variable(4)),
                                            )
                                        )
                                    ),
                                ),
                                Abstraction(Variable(2)),
                            ),
                            Abstraction(Variable(1)),
                        )
                    )
                )
            ),
        ),
        # fac
        # λn.λf.n(λf.λn.n(f(λf.λx.n f(f x))))(λx.f)(λx.x)
        (
            """
            ###################################
             #
            ###################################
             #                           #
             #  ####################### ### ###
             #       #                   #   #
             #  #######################  #   #
             #   #   #   #               #   #
             #   #   #  ###############  #   #
             #   #   #   #   #   #       #   #
             #   #   #  ###############  #   #
             #   #   #   #   #   #   #   #   #
             #   #   #   #####   #####   #   #
             #   #   #   #       #       #   #
             #   #   #   #########       #   #
             #   #   #   #               #   #
             #   #   #####               #   #
             #   #   #                   #   #
             #   #####                   #   #
             #   #                       #   #
             #####                       #   #
             #                           #   #
             #############################   #
             #                               #
             #################################
             #
             #
            """,
            Abstraction(
                Abstraction(
                    Application(
                        Application(
                            Application(
                                Variable(2),
                                Abstraction(
                                    Abstraction(
                                        Application(
                                            Variable(1),
                                            Application(
                                                Variable(2),
                                                Abstraction(
                                                    Abstraction(
                                                        Application(
                                                            Application(
                                                                Variable(3),
                                                                Variable(2),
                                                            ),
                                                            Application(
                                                                Variable(2),
                                                                Variable(1),
                                                            ),
                                                        )
                                                    )
                                                ),
                                            ),
                                        )
                                    )
                                ),
                            ),
                            Abstraction(Variable(2)),
                        ),
                        Abstraction(Variable(1)),
                    )
                )
            ),
        ),
        (
            """
            ###################################
             #
            ###################################
             #                           #
             #  ####################### ### ###
             #       #                   #   #
             #  #######################  #   #
             #   #   #   #               #   #
             #   #   #  ###############  #   #
             #   #   #   #   #   #       #   #
             #   #   #  ###############  #   #
             #   #   #   #   #   #   #   #   #
             #   #   #   #####   #####   #   #
             #   #   #       #   #       #   #
             #   #   #       #####       #   #
             #   #   #       #           #   #
             #   #   #########           #   #
             #   #   #                   #   #
             #   #####                   #   #
             #   #                       #   #
             #####                       #   #
                 #                       #   #
                 #########################   #
                                         #   #
                                         #####
            """,
            Abstraction(
                Abstraction(
                    Application(
                        Application(
                            Application(
                                Variable(2),
                                Abstraction(
                                    Abstraction(
                                        Application(
                                            Variable(1),
                                            Application(
                                                Variable(2),
                                                Abstraction(
                                                    Abstraction(
                                                        Application(
                                                            Application(
                                                                Variable(3),
                                                                Variable(2),
                                                            ),
                                                            Application(
                                                                Variable(2),
                                                                Variable(1),
                                                            ),
                                                        )
                                                    )
                                                ),
                                            ),
                                        )
                                    )
                                ),
                            ),
                            Abstraction(Variable(2)),
                        ),
                        Abstraction(Variable(1)),
                    )
                )
            ),
        ),
        # fib
        # λn.λf.n(λc.λa.λb.c b(λx.a (b x)))(λx.λy.x)(λx.x)f
        (
            """
            ###################################
             #
            ###################################
             #                               #
             #  ################### ### ###  #
             #   #                   #   #   #
             #  ################### ###  #   #
             #   #       #           #   #   #
             #  ###################  #   #   #
             #   #   #   #   #       #   #   #
             #   #####  ###########  #   #   #
             #   #       #   #   #   #   #   #
             #   #       #   #####   #   #   #
             #   #       #   #       #   #   #
             #   #       #####       #   #   #
             #   #       #           #   #   #
             #   #########           #   #   #
             #   #                   #   #   #
             #####                   #   #   #
             #                       #   #   #
             #########################   #   #
             #                           #   #
             #############################   #
             #                               #
             #################################
             #
             #
            """,
            Abstraction(
                Abstraction(
                    Application(
                        Application(
                            Application(
                                Application(
                                    Variable(2),
                                    Abstraction(
                                        Abstraction(
                                            Abstraction(
                                                Application(
                                                    Application(
                                                        Variable(3),
                                                        Variable(1),
                                                    ),
                                                    Abstraction(
                                                        Application(
                                                            Variable(3),
                                                            Application(
                                                                Variable(2),
                                                                Variable(1),
                                                            ),
                                                        )
                                                    ),
                                                )
                                            )
                                        )
                                    ),
                                ),
                                Abstraction(Abstraction(Variable(2))),
                            ),
                            Abstraction(Variable(1)),
                        ),
                        Variable(1),
                    )
                )
            ),
        ),
        (
            """
            ###################################
             #
            ###################################
             #                               #
             #  ################### ### ###  #
             #   #                   #   #   #
             #  ################### ###  #   #
             #   #       #           #   #   #
             #  ###################  #   #   #
             #   #   #   #   #       #   #   #
             #   #####  ###########  #   #   #
             #       #   #   #   #   #   #   #
             #       #   #   #####   #   #   #
             #       #   #   #       #   #   #
             #       #   #####       #   #   #
             #       #   #           #   #   #
             #       #####           #   #   #
             #       #               #   #   #
             #########               #   #   #
                     #               #   #   #
                     #################   #   #
                                     #   #   #
                                     #####   #
                                         #   #
                                         #####
            """,
            Abstraction(
                Abstraction(
                    Application(
                        Application(
                            Application(
                                Application(
                                    Variable(2),
                                    Abstraction(
                                        Abstraction(
                                            Abstraction(
                                                Application(
                                                    Application(
                                                        Variable(3),
                                                        Variable(1),
                                                    ),
                                                    Abstraction(
                                                        Application(
                                                            Variable(3),
                                                            Application(
                                                                Variable(2),
                                                                Variable(1),
                                                            ),
                                                        )
                                                    ),
                                                )
                                            )
                                        )
                                    ),
                                ),
                                Abstraction(Abstraction(Variable(2))),
                            ),
                            Abstraction(Variable(1)),
                        ),
                        Variable(1),
                    )
                )
            ),
        ),
        # omega
        # (λx.x x)(λx.x x)
        (
            """
            ####### #######
             #   #   #   #
             #####   #####
             #       #
             #########
             #
             #
            """,
            Application(
                Abstraction(Application(Variable(1), Variable(1))),
                Abstraction(Application(Variable(1), Variable(1))),
            ),
        ),
        (
            """
            ####### #######
             #   #   #   #
             #####   #####
                 #   #
                 #####
            """,
            Application(
                Abstraction(Application(Variable(1), Variable(1))),
                Abstraction(Application(Variable(1), Variable(1))),
            ),
        ),
    ],
)
def test_parse_diagram(diagram_str: str, want_ast: Expression):
    diagram = LambdaDiagram.from_str(diagram_str)
    assert parse_diagram(diagram) == want_ast
