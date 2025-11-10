from config.substitution_modules.substitution_module import (
    SubstitutionModule,
    register_substitution_module,
)


@register_substitution_module
class NumberSubstitution(SubstitutionModule):

    def __init__(self) -> None:
        self.__invoice_number: int = 0

    def match(self) -> str:
        return r"\b\d+\b"  # One or more numbers

    @classmethod
    def name(cls) -> str:
        return "number"

    def to_string(self) -> str:
        return self.__invoice_number.__str__()

    def set_number(self, invoice_number: int) -> None:
        self.__invoice_number = invoice_number
