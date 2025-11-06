from datetime import date
from config.pattern_modules.pattern_module import PatternModule
import re

class StaticStringPattern(PatternModule):

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

    def is_mandatory(self):
        return False