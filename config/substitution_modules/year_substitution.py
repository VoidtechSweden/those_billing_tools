from datetime import date
from config.substitution_modules.substitution_module import (
    SubstitutionModule,
    register_substitution_module,
)


@register_substitution_module
class YearSubstitution(SubstitutionModule):

    def match(self):
        return r"\b\d{4}\b"  # Four numbers only

    @classmethod
    def name(cls):
        return "year"

    def to_string(self):
        return date.today().year.__str__()
