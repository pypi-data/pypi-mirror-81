import python_dice.src.python_dice_expression.abs_expression as abs_expression
import python_dice.src.python_dice_expression.add_expression as add_expression
import python_dice.src.python_dice_expression.binary_operator_expression as binary_operator_expression
import python_dice.src.python_dice_expression.constant_binary_expression as constant_binary_expression
import python_dice.src.python_dice_expression.constant_integer_expression as constant_integer_expression
import python_dice.src.python_dice_expression.dice_expression as dice_expression
import python_dice.src.python_dice_expression.drop_keep_expression as drop_keep_expression
import python_dice.src.python_dice_expression.get_var_expression as get_var_expression
import python_dice.src.python_dice_expression.integer_division_expression as integer_division_expression
import python_dice.src.python_dice_expression.minmax_expression as minmax_expression
import python_dice.src.python_dice_expression.multiply_expression as multiply_expression
import python_dice.src.python_dice_expression.not_expression as not_expression
import python_dice.src.python_dice_expression.parentheses_enclosed_expression as parentheses_enclosed_expression
import python_dice.src.python_dice_expression.subtract_expression as subtract_expression
import python_dice.src.python_dice_expression.var_assignment_expression as var_assignment_expression
import python_dice.src.python_dice_syntax.abs_syntax as abs_syntax
import python_dice.src.python_dice_syntax.add_syntax as add_syntax
import python_dice.src.python_dice_syntax.assignment_syntax as assignment_syntax
import python_dice.src.python_dice_syntax.binary_operator_syntax as binary_operator_syntax
import python_dice.src.python_dice_syntax.close_parenthesis_syntax as close_parenthesis_syntax
import python_dice.src.python_dice_syntax.comma_syntax as comma_syntax
import python_dice.src.python_dice_syntax.constant_binary_syntax as constant_binary_syntax
import python_dice.src.python_dice_syntax.constant_integer_syntax as constant_integer_syntax
import python_dice.src.python_dice_syntax.dice_syntax as dice_syntax
import python_dice.src.python_dice_syntax.drop_keep_syntax as drop_keep_syntax
import python_dice.src.python_dice_syntax.integer_division_syntax as integer_division_syntax
import python_dice.src.python_dice_syntax.min_max_syntax as min_max_syntax
import python_dice.src.python_dice_syntax.multiply_syntax as multiply_syntax
import python_dice.src.python_dice_syntax.name_syntax as name_syntax
import python_dice.src.python_dice_syntax.not_syntax as not_syntax
import python_dice.src.python_dice_syntax.open_parenthesis_syntax as open_parenthesis_syntax
import python_dice.src.python_dice_syntax.subtract_syntax as subtract_syntax
import python_dice.src.python_dice_syntax.var_syntax as var_syntax

LEXER_SYNTAX = [
    open_parenthesis_syntax.OpenParenthesisSyntax,
    close_parenthesis_syntax.CloseParenthesisSyntax,
    comma_syntax.CommaSyntax,
    not_syntax.NotSyntax,
    drop_keep_syntax.DropKeepSyntax,
    dice_syntax.DiceSyntax,
    binary_operator_syntax.BinaryOperatorSyntax,
    constant_integer_syntax.ConstantIntegerSyntax,
    constant_binary_syntax.ConstantBinarySyntax,
    add_syntax.AddSyntax,
    subtract_syntax.SubtractSyntax,
    multiply_syntax.MultiplySyntax,
    integer_division_syntax.IntegerDivisionSyntax,
    min_max_syntax.MinMaxSyntax,
    abs_syntax.AbsSyntax,
    assignment_syntax.AssignmentSyntax,
    var_syntax.VarSyntax,
    name_syntax.NameSyntax,
]

PARSER_EXPRESSIONS = [
    parentheses_enclosed_expression.ParenthesisEnclosedExpression,
    not_expression.NotExpression,
    drop_keep_expression.DropKeepExpression,
    dice_expression.DiceExpression,
    constant_integer_expression.ConstantIntegerExpression,
    constant_binary_expression.ConstantBinaryExpression,
    add_expression.AddExpression,
    subtract_expression.SubtractExpression,
    multiply_expression.MultiplyExpression,
    integer_division_expression.IntegerDivisionExpression,
    binary_operator_expression.BinaryOperatorExpression,
    minmax_expression.MinMaxExpression,
    abs_expression.AbsExpression,
    var_assignment_expression.VarAssignmentExpression,
    get_var_expression.GetVarExpression,
]

PRECEDENCE = [
    ("nonassoc", [var_syntax.VarSyntax.get_token_name()]),
    ("left", [assignment_syntax.AssignmentSyntax.get_token_name()]),
    ("left", [open_parenthesis_syntax.OpenParenthesisSyntax.get_token_name()]),
    ("left", [not_syntax.NotSyntax.get_token_name()]),
    (
        "left",
        [
            add_syntax.AddSyntax.get_token_name(),
            subtract_syntax.SubtractSyntax.get_token_name(),
        ],
    ),
    (
        "left",
        [
            integer_division_syntax.IntegerDivisionSyntax.get_token_name(),
            multiply_syntax.MultiplySyntax.get_token_name(),
        ],
    ),
    ("left", [binary_operator_syntax.BinaryOperatorSyntax.get_token_name()]),
]
