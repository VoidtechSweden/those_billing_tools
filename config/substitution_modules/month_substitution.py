from datetime import date
from config.substitution_modules.substitution_module import (
    SubstitutionModule,
    register_substitution_module,
)

month_names_swe = [
    "Januari",
    "Februari",
    "Mars",
    "April",
    "Maj",
    "Juni",
    "Juli",
    "Augusti",
    "September",
    "Oktober",
    "November",
    "December",
]
month_names_eng = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


@register_substitution_module
class MonthSubstitution(SubstitutionModule):
    """Substitution module for month in human-readable format."""

    def __init__(self, language: str = "swe"):
        assert language.lower() in [
            "swe",
            "eng",
        ], "Language must be either 'swe' or 'eng'"
        self.__language = language
        super().__init__(language)

    def __get_month_name(self, month_number: int) -> str:
        if self.__language.lower() == "swe":
            return month_names_swe[month_number - 1]
        else:
            return month_names_eng[month_number - 1]

    def match(self) -> str:
        if self.__language.lower() == "swe":
            pattern = "|".join(month_names_swe)
        else:
            pattern = "|".join(month_names_eng)
        return f"({pattern})"

    @classmethod
    def name(cls) -> str:
        return "month"

    def to_string(self) -> str:
        return self.__get_month_name(date.today().month)
