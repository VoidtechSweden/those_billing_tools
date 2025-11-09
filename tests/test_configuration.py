import configparser
import os

import pytest
from config.config import Configuration
import tempfile
import contextlib

CONFIG_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "../template.config")


@contextlib.contextmanager
def temporary_config(updated_fields=[], invalid=False):
    """Create and use temporary configuration file for testing purposes."""

    config = configparser.ConfigParser()
    config.read(CONFIG_TEMPLATE_PATH)

    for section, option, value in updated_fields:
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, option, value)

    if invalid:
        config.remove_option("identification", "company")

    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".config") as tmp:
        config.write(tmp)
        tmp.flush()
        tmp.seek(0)
        Configuration.force_config_file(tmp.name)
        yield
    Configuration.reset()
    os.remove(tmp.name)


def test_template_configuration():
    """
    TEST: Loading the template configuration from file

    EXPECTED: Loaded successfully. A Configuration value matches in the template
    """

    with temporary_config():
        assert Configuration.get("identification", "company") == "My Company"


def test_invalid_configuration():
    """
    TEST: Loading a configuration file that is missing a field from the template

    EXPECTED: AssertionError is raised
    """

    with temporary_config(invalid=True):
        with pytest.raises(AssertionError):
            Configuration.get("identification", "name")


def test_name_company_substitution():
    """
    TEST: Loading a configuration file with the {name} and {company} substitution patterns

    EXPECTED: The substitutions are correctly applied
    """

    name = "Alexander"
    company = "testcompany"
    expected_mail = f"{name}@{company}.se"

    config_fields = [
        ("identification", "name", name),
        ("identification", "company", company),
        ("identification", "email", "{name}@{company}.se"),
    ]

    with temporary_config(updated_fields=config_fields):
        assert Configuration.get("identification", "name") == name
        assert Configuration.get("identification", "company") == company
        assert Configuration.get("identification", "email") == expected_mail

    # TODO test more configuration aspects, for example invoice pattern parsing
