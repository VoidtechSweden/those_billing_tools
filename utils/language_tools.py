from enum import Enum


class Language(Enum):
    SWE = "swe"
    ENG = "eng"

    @staticmethod
    def from_string(language_str: str) -> "Language":
        """Convert a string to a Language enum value.

        Args:
            language_str (str): The language string ("swe" or "eng").

        Returns:
            Language: The corresponding Language enum value.
        """
        language_str = language_str.lower()
        if language_str == "swe":
            return Language.SWE
        elif language_str == "eng":
            return Language.ENG
        else:
            assert False, f"Unsupported language string: {language_str}"


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


def __list_pattern(names: list[str]) -> str:
    pattern = "|".join(names)
    return f"({pattern})"


def month_to_string(month_number: int, language: Language = Language.SWE) -> str:
    """Convert a month number to its human-readable name in the specified language.

    Args:
        month_number (int): The month number (1-12).
        language (Language): The language enum value (Language.SWE for Swedish, Language.ENG for English).

    Returns:
        str: The human-readable month name.
    """

    if language == Language.SWE:
        return month_names_swe[month_number - 1]
    else:
        return month_names_eng[month_number - 1]


def months_pattern(language: Language = Language.SWE) -> str:
    """Get a regex pattern matching all month names in the specified language.

    Args:
        language (Language): The language enum value (Language.SWE for Swedish, Language.ENG for English).

    Returns:
        str: A regex pattern matching all month names.
    """
    if language == Language.SWE:
        pattern = __list_pattern(month_names_swe)
    else:
        pattern = __list_pattern(month_names_eng)
    return pattern
