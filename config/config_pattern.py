import re
from config.substitution_modules.substitution_module import SubstitutionModuleRegistry


class ConfigPattern:

    def __init__(self):
        self.__modules = []

    def create(self, string):
        """Given a pattern string, extract and return a list of SubstitutionModule instances representing the pattern."""

        def create_substitution_module(string):
            if string.startswith("{") and string.endswith("}"):
                substitution_name = string[1:-1]
                for (
                    substitution_class
                ) in SubstitutionModuleRegistry.get_registered_modules():
                    if substitution_class.name() == substitution_name:
                        return substitution_class()
                assert False, f"Unknown substitution '{substitution_name}'"
            else:
                from config.substitution_modules.staticstring_substitution import (
                    StaticStringSubstitution,
                )

                return StaticStringSubstitution(string)

        current = ""
        in_braces = False
        for char in string:
            if char == "{":
                if in_braces:
                    current += char
                else:
                    in_braces = True
                    if current:
                        self.__modules.append(create_substitution_module(current))
                    current = char
            elif char == "}":
                if in_braces:
                    in_braces = False
                    current += char
                    self.__modules.append(create_substitution_module(current))
                    current = ""
                else:
                    current += char
            else:
                current += char
        if current:
            self.__modules.append(create_substitution_module(current))

    def contains_number(self):
        for module in self.__modules:
            if module.name() == "number":
                return True
        return False

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
        assert (
            self.contains_number()
        ), "Pattern does not contain a 'number' substitution module"

        for module in self.__modules:
            if module.name() == "number":
                module.set_number(number)

    def find_substitution_value(self, targetmodule, text):
        """Find and return the value of the first occurrence of the pattern module in the given text."""

        start_regexp = ""
        module_regexp = ""
        for module in self.__modules:
            if module.name() == targetmodule:
                module_regexp = module.match()
                break
            start_regexp += module.match()

        # Find the value that starts after the start_regexp and matches the module_regexp
        prefix = re.search(start_regexp, text).group(0)

        # remove the found prefix from the text
        text = text[len(prefix) :]

        return re.search(module_regexp, text).group(0)
