import typing

import rply

import python_dice.interface.i_probability_distribution as i_probability_distribution
import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution


class ConstantBinaryExpression(i_dice_expression.IDiceExpression):
    TOKEN_RULE = """expression : CONSTANT_BINARY"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator,
    ) -> typing.Callable:
        @parser_generator.production(ConstantBinaryExpression.TOKEN_RULE)
        def constant_binary(_, tokens) -> i_dice_expression.IDiceExpression:
            return ConstantBinaryExpression(tokens[0].value)

        return constant_binary

    def __init__(self, binary_string: str):
        self._binary_string = binary_string

    def _get_value(self) -> int:
        return 1 if self._binary_string == "True" else 0

    def roll(self) -> int:
        return self._get_value()

    def max(self) -> int:
        return self._get_value()

    def min(self) -> int:
        return self._get_value()

    def __str__(self) -> str:
        return self._binary_string

    def estimated_cost(self) -> int:
        return 2

    def get_probability_distribution(
        self,
    ) -> i_probability_distribution.IProbabilityDistribution:
        return probability_distribution.ProbabilityDistribution({self._get_value(): 1})
