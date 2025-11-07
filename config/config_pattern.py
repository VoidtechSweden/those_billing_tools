import re
from config.pattern_modules.pattern_module import PatternModuleRegistry


class ConfigPattern:

    def __init__(self):
        self.__modules = []

    def create(self, string):
        """Given a pattern string, extract and return a list of PatternModule instances representing the pattern."""

        def create_pattern_module(string):
            if string.startswith("{") and string.endswith("}"):
                pattern_name = string[1:-1]
                for pattern_class in PatternModuleRegistry.get_registered_modules():
                    if pattern_class.name() == pattern_name:
                        return pattern_class()
                assert False, f"Unknown pattern '{pattern_name}'"
            else:
                from config.pattern_modules.staticstring_pattern import (
                    StaticStringPattern,
                )

                return StaticStringPattern(string)

        current = ""
        in_braces = False
        for char in string:
            if char == "{":
                if in_braces:
                    current += char
                else:
                    in_braces = True
                    if current:
                        self.__modules.append(create_pattern_module(current))
                    current = char
            elif char == "}":
                if in_braces:
                    in_braces = False
                    current += char
                    self.__modules.append(create_pattern_module(current))
                    current = ""
                else:
                    current += char
            else:
                current += char
        if current:
            self.__modules.append(create_pattern_module(current))

    def get_regexp(self):
        regexp = ""
        for module in self.__modules:
            regexp += module.match()
        return regexp

    def to_string(self):
        pattern_string = ""
        for module in self.__modules:
            pattern_string += module.to_string()
        return pattern_string

    def to_string_with_number(self, number):
        self.set_number(number)
        string = self.to_string()
        return string

    def set_number(self, number):
        for module in self.__modules:
            if module.name() == "number":
                module.set_number(number)

    def find_pattern(self, targetmodule, text):
        """Find and return the value of the first occurrence of the pattern module in the given text."""

        start_regexp = ""
        module_regexp = ""
        for module in self.__modules:
            if module.name() == targetmodule:
                module_regexp = module.match()
                break
            start_regexp += module.match()

        # Find the value that starts after the start_regexp and matches the module_regexp
        pattern_regexp = f"(?<={start_regexp})"
        prefix = re.search(pattern_regexp, text).group(0)

        # remove the found prefix from the text
        text = text[len(prefix) :]

        return re.search(module_regexp, text).group(0)
