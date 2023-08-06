_NUMBER_OF_DICE = r"\d*"
_DICE_SYMBOL = r"d"

_DICE_NUM_TYPE = r"\d+"
_PERCENTILE_TYPE = r"%"
_FATE_TYPE = r"F"
_CUSTOM_TYPE_ENTRY = r"(-?\d+--?\d+(\*\d+)?|-?\d+(\*\d+)?)"
_CUSTOM_TYPE = (
    rf"\[(\s*{_CUSTOM_TYPE_ENTRY}\s*,\s*)*\s*{_CUSTOM_TYPE_ENTRY}\s*(,?)\s*\]"
)

_DICE_TYPE = f"({_DICE_NUM_TYPE}|{_PERCENTILE_TYPE}|{_FATE_TYPE}|{_CUSTOM_TYPE})"
_DROP_KEEP = r"[kd]\d+"

DICE_SYNTAX = _NUMBER_OF_DICE + _DICE_SYMBOL + _DICE_TYPE
DROP_KEEP_DICE_SYNTAX = DICE_SYNTAX + _DROP_KEEP
