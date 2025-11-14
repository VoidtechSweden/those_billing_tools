import re
from config.substitution_modules.substitution_module import (
    SubstitutionModule,
    SubstitutionModuleRegistry,
)
from config.substitution_modules.staticstring_substitution import (
    StaticStringSubstitution,
)


class ConfigPattern:

    def __init__(self):
        self.__modules = []

    def create(self, string, custom_placeholders):
        """Given a pattern string, extract and return a list of SubstitutionModule instances representing the pattern."""

        def create_substitution_module(
            string: str, custom_placeholders
        ) -> SubstitutionModule:
            if string.startswith("{") and string.endswith("}"):
                # split on colon to allow parameters
                substitution_split = string[1:-1].split(":")
                substitution_name = substitution_split[0]
                substitution_param = ""
                if len(substitution_split) > 1:
                    substitution_param = substitution_split[1]

                # Find built-in substitution modules
                for (
                    substitution_class
                ) in SubstitutionModuleRegistry.get_registered_modules():
                    if substitution_class.name() == substitution_name:
                        return substitution_class(substitution_param)

                # Find custom configured placeholders
                custom_value = ""
                for key, value in custom_placeholders:
                    if key == substitution_name:
                        custom_value = value
                        break
                assert custom_value, f"Unknown placeholder '{substitution_name}'"

                return StaticStringSubstitution(custom_value)
            else:
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
                        self.__modules.append(
                            create_substitution_module(current, custom_placeholders)
                        )  # Adds static string before {
                    current = char
            elif char == "}":
                if in_braces:
                    in_braces = False
                    current += char
                    self.__modules.append(
                        create_substitution_module(current, custom_placeholders)
                    )  # Adds substitution module based on whats inside {}
                    current = ""
                else:
                    current += char
            else:
                current += char
        if current:
            self.__modules.append(
                create_substitution_module(current, custom_placeholders)
            )  # Adds remaining static string

    def contains_number(self) -> bool:
        for module in self.__modules:
            if module.name() == "number":
                return True
        return False

    def get_regexp(self) -> str:
        regexp = "(?i)"  # Add case insensitivity at the start
        for module in self.__modules:
            regexp += module.match()
        return regexp

    def to_string(self) -> str:
        pattern_string = ""
        for module in self.__modules:
            pattern_string += module.to_string()
        return pattern_string

    def to_string_with_number(self, number: int) -> str:
        self.set_number(number)
        string = self.to_string()
        return string

    def set_number(self, number: int) -> None:
        assert (
            self.contains_number()
        ), "Pattern does not contain a 'number' substitution module"

        for module in self.__modules:
            if module.name() == "number":
                module.set_number(number)

    def find_substitution_value(self, targetmodule: str, text: str) -> str:
        """Find and return the value of the first occurrence of the pattern module in the given text."""

        start_regexp = ""
        module_regexp = ""
        for module in self.__modules:
            if module.name() == targetmodule:
                module_regexp = module.match()
                break
            start_regexp += module.match()

        # Find the value that starts after the start_regexp and matches the module_regexp
        match = re.search(start_regexp, text)
        assert match is not None, f"Pattern '{start_regexp}' not found in {text}"
        prefix: str = match.group(0)

        # remove the found prefix from the text
        remaining_text: str = text[len(prefix) :]
        match2 = re.search(module_regexp, remaining_text)
        assert (
            match2 is not None
        ), f"Pattern module '{targetmodule}' not found in {remaining_text}"
        found: str = match2.group(0)

        return found
