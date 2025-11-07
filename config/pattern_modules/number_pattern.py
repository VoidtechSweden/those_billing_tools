from config.pattern_modules.pattern_module import PatternModule, register_pattern_module


@register_pattern_module
class NumberPattern(PatternModule):

    def __init__(self):
        self.__invoice_number = None

    def match(self):
        return r"\b\d+\b"  # One or more numbers

    @classmethod
    def name(cls):
        return "number"

    def to_string(self):
        return self.__invoice_number.__str__()

    def is_mandatory(self):
        return True

    def set_number(self, invoice_number):
        self.__invoice_number = invoice_number
