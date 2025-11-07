import configparser
import os
from config.config_pattern import ConfigPattern


class Configuration:

    _CONFIG = None
    _INVOICE_PATTERN = ConfigPattern()

    @staticmethod
    def __load():
        config_file = "my.config"

        if not os.path.exists(config_file):
            assert False, f"Configuration file '{config_file}' not found."

        # load template config and check that all required fields are present
        template_file = "template.config"
        if not os.path.exists(template_file):
            assert False, f"Template configuration file '{template_file}' not found."

        # Load configs
        template = configparser.ConfigParser()
        template.read(template_file)
        Configuration._CONFIG = configparser.ConfigParser()
        Configuration._CONFIG.read(config_file)

        # Check that my config contains all fields from the template
        for section in template.sections():
            for option in template.options(section):
                if not Configuration._CONFIG.has_option(section, option):
                    assert False, f"Missing configuration for [{section}] {option}"

        # Handle config values with substitute patterns
        for section in Configuration._CONFIG.sections():
            for option in Configuration._CONFIG.options(section):
                value = Configuration._CONFIG.get(section, option)
                if section == "billing" and option == "invoice_pattern":
                    # Save invoice pattern separately
                    Configuration._INVOICE_PATTERN.create(value)

                    # validate that pattern contains mandatory 'number' substitution module
                    assert (
                        Configuration._INVOICE_PATTERN.contains_number()
                    ), "Invoice name pattern must contain a '{number}' substitution module"

                elif "{" in value and "}" in value:
                    replacement_pattern = ConfigPattern()
                    replacement_pattern.create(value)
                    Configuration._CONFIG.set(
                        section, option, replacement_pattern.to_string()
                    )

    @staticmethod
    def __internal_get(section, option, type=str):
        if Configuration._CONFIG is None:
            Configuration.__load()
        try:
            if type == bool:
                value = Configuration._CONFIG.getboolean(section, option)
            elif type == int:
                value = Configuration._CONFIG.getint(section, option)
            else:
                value = Configuration._CONFIG.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            value = None
            assert False, f"Missing configuration for [{section}] {option}"

        return value

    @staticmethod
    def get(section, option):
        return Configuration.__internal_get(section, option, str)

    @staticmethod
    def getboolean(section, option):
        return Configuration.__internal_get(section, option, bool)

    @staticmethod
    def getint(section, option):
        return Configuration.__internal_get(section, option, int)

    @staticmethod
    def get_invoice_pattern():
        return Configuration._INVOICE_PATTERN
