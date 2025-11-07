from config.substitution_modules.substitution_module import (
    SubstitutionModule,
    register_substitution_module,
)


@register_substitution_module
class NumberSubstitution(SubstitutionModule):

    def __init__(self):
        self.__invoice_number = None

    def match(self):
        return r"\b\d+\b"  # One or more numbers

    @classmethod
    def name(cls):
        return "number"

    def to_string(self):
        return self.__invoice_number.__str__()

    def set_number(self, invoice_number):
        self.__invoice_number = invoice_number
