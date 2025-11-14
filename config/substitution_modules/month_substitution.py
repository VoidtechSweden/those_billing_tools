from datetime import date
from config.substitution_modules.substitution_module import (
    SubstitutionModule,
    register_substitution_module,
)
from utils import language_tools


@register_substitution_module
class MonthSubstitution(SubstitutionModule):
    """Substitution module for month in human-readable format."""

    def __init__(self, language: str = "swe"):
        if language == "":
            language = "swe"
        self.__language = language_tools.Language.from_string(language)
        super().__init__(language)

    def __get_month_name(self, month_number: int) -> str:
        return language_tools.month_to_string(month_number, self.__language)

    def match(self) -> str:
        return language_tools.months_pattern(self.__language)

    @classmethod
    def name(cls) -> str:
        return "month"

    def to_string(self) -> str:
        return self.__get_month_name(date.today().month)
