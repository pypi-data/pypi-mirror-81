import typing

import rply

import python_dice.interface.i_probability_distribution as i_probability_distribution
import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression


class SubtractExpression(i_dice_expression.IDiceExpression):
    TOKEN_RULE = """expression : expression SUBTRACT expression"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator,
    ) -> typing.Callable:
        @parser_generator.production(SubtractExpression.TOKEN_RULE)
        def subtract(_, tokens) -> i_dice_expression.IDiceExpression:
            return SubtractExpression(tokens[0], tokens[2])

        return subtract

    def __init__(
        self,
        expression_one: i_dice_expression.IDiceExpression,
        expression_two: i_dice_expression.IDiceExpression,
    ):
        self._expression_one = expression_one
        self._expression_two = expression_two

    def roll(self) -> int:
        return self._expression_one.roll() - self._expression_two.roll()

    def max(self) -> int:
        return self.get_probability_distribution().max()

    def min(self) -> int:
        return self.get_probability_distribution().min()

    def __str__(self) -> str:
        return f"{str(self._expression_one)} - {str(self._expression_two)}"

    def estimated_cost(self) -> int:
        return (
            self._expression_one.estimated_cost()
            + self._expression_two.estimated_cost()
        )

    def get_probability_distribution(
        self,
    ) -> i_probability_distribution.IProbabilityDistribution:
        return (
            self._expression_one.get_probability_distribution()
            - self._expression_two.get_probability_distribution()
        )
