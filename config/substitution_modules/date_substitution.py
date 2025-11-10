from datetime import date
from config.substitution_modules.substitution_module import (
    SubstitutionModule,
    register_substitution_module,
)


@register_substitution_module
class DateSubstitution(SubstitutionModule):
    """Substitution module for current date in YYYY-MM-DD format."""

    def match(self) -> str:
        return r"\b\d{4}-\d{2}-\d{2}\b"  # Date in YYYY-MM-DD format

    @classmethod
    def name(cls) -> str:
        return "date"

    def to_string(self) -> str:
        return date.today().strftime("%Y-%m-%d")
