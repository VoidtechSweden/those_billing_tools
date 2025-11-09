import configparser
import os
from config.config_pattern import ConfigPattern


class Configuration:

    _CONFIG = None
    _INVOICE_PATTERN = ConfigPattern()
    CONFIG_FILE = "my.config"

    def reset():
        """Reset the loaded configuration"""
        Configuration._CONFIG = None

    def force_config_file(config_file):
        """Force the use of a specific configuration file"""
        Configuration.reset()
        Configuration.CONFIG_FILE = config_file

    @staticmethod
    def __load():
        """Load the configuration from file and validate required fields"""

        if not os.path.exists(Configuration.CONFIG_FILE):
            assert False, f"Configuration file '{Configuration.CONFIG_FILE}' not found."

        template_file = "template.config"
        if not os.path.exists(template_file):
            assert False, f"Template configuration file '{template_file}' not found."

        print(f"Loading configuration from '{Configuration.CONFIG_FILE}'")

        # Load configs
        template = configparser.ConfigParser()
        template.read(template_file)
        Configuration._CONFIG = configparser.ConfigParser()
        Configuration._CONFIG.read(Configuration.CONFIG_FILE)

        # Check that my config contains all fields from the template
        for section in template.sections():
            for option in template.options(section):
                if not Configuration._CONFIG.has_option(section, option):
                    assert (
                        False
                    ), f"Missing configuration from template: [{section}] [{option}]"

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
            assert False, f"Missing configuration for [{section}] [{option}]"

        return value

    @staticmethod
    def get(section, option):
        """
        Get a configuration value as a string
        """
        return Configuration.__internal_get(section, option, str)

    @staticmethod
    def getboolean(section, option):
        """Get a configuration value as a boolean"""
        return Configuration.__internal_get(section, option, bool)

    @staticmethod
    def getint(section, option):
        """Get a configuration value as an integer"""
        return Configuration.__internal_get(section, option, int)

    @staticmethod
    def get_invoice_pattern():
        """Get the invoice name pattern as a ConfigPattern object"""
        return Configuration._INVOICE_PATTERN
