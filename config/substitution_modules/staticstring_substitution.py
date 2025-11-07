from config.substitution_modules.substitution_module import SubstitutionModule
import re


class StaticStringSubstitution(SubstitutionModule):
    """A dummy module that always matches a static string"""

    def __init__(self, static_string):
        super().__init__()

        self.__static_string = static_string
        self.__static_string_escaped = re.escape(static_string)

    def match(self):
        return self.__static_string_escaped

    @classmethod
    def name(cls):
        return "staticstring"

    def to_string(self):
        return self.__static_string
