import configparser
import os
import re

import pytest
from config.config import Configuration
import tempfile
import contextlib
from datetime import date

from utils import language_tools

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

    tmpfile = None
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".config") as tmp:
        tmpfile = tmp.name
        config.write(tmp)
        tmp.flush()
        tmp.seek(0)
        Configuration.instance(tmp.name).reload_config_file(
            tmp.name
        )  # Needed to reload singleton
        yield
    os.remove(tmpfile)


def test_template_configuration():
    """
    TEST: Loading the template configuration from file

    EXPECTED: Loaded successfully. A Configuration value matches in the template
    """

    with temporary_config():
        assert Configuration.instance().identification.company == "My Company"


def test_invalid_configuration():
    """
    TEST: Loading a configuration file that is missing a field from the template

    EXPECTED: AssertionError is raised
    """

    with pytest.raises(AssertionError):
        with temporary_config(invalid=True):
            pass


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
        assert Configuration.instance().identification.name == name
        assert Configuration.instance().identification.company == company
        assert Configuration.instance().identification.email == expected_mail


def test_currentdir_substitution():
    """
    TEST: Loading a configuration file with the {currentdir} substitution pattern

    EXPECTED: The substitutions are correctly applied
    """

    config_fields = [
        ("billing", "invoices_path", "{currentdir}/../testfolder/"),
    ]

    with temporary_config(updated_fields=config_fields):
        assert Configuration.instance().billing.invoices_path.startswith(os.getcwd())
        assert Configuration.instance().billing.invoices_path.endswith("../testfolder/")


class TestInvoicePattern:

    @pytest.mark.parametrize(
        "language",
        [
            language_tools.Language.SWE,
            language_tools.Language.ENG,
        ],
    )
    @pytest.mark.parametrize(
        "divider",
        [
            " ",
            "-",
            ".",
            "_",
        ],
    )
    def test_substitution(self, divider, language):
        """
        TEST: Loading a configuration file with the invoice pattern substitution
              parametrized with different dividers and languages

        EXPECTED: The invoice pattern is correctly parsed and usable to generate invoice names
        """

        invoice_number = 123
        company = "testcompany"
        expected_month = language_tools.month_to_string(date.today().month, language)
        expected_date = date.today().strftime("%Y-%m-%d")
        expected_invoice_name = f"{company}{divider}{expected_date}{divider}{expected_month}{divider}FAKTURA{divider}{invoice_number}"

        config_pattern = f"{{company}}{divider}{{date}}{divider}{{month:{language.value}}}{divider}FAKTURA{divider}{{number}}"
        config_fields = [
            ("billing", "invoice_pattern", config_pattern),
            ("identification", "company", company),
        ]

        with temporary_config(updated_fields=config_fields):
            invoice_pattern = Configuration.instance().billing.invoice_pattern
            invoice_pattern.set_number(invoice_number)

            # Check that the pattern contains the number substitution
            assert invoice_pattern.contains_number()

            # Verify that the pattern works correctly and generates the expected invoice name
            assert invoice_pattern.to_string() == expected_invoice_name
            assert invoice_pattern.to_string_with_number(
                99
            ) == expected_invoice_name.replace(str(invoice_number), "99")

            # Verify that the regexp works correctly and can be matched to the expected invoice name
            regexp = invoice_pattern.get_regexp()
            print(f"Generated regexp: {regexp}")
            match = re.match(regexp, expected_invoice_name)
            assert match is not None
            assert match.group(0) == expected_invoice_name

            # Verify that the regexp is case insensitive
            match_upper = re.match(regexp, expected_invoice_name.upper())
            assert match_upper is not None
            assert match_upper.group(0) == expected_invoice_name.upper()

            # Use the pattern to find the number value from the expected invoice name
            found_number = invoice_pattern.find_substitution_value(
                "number", expected_invoice_name
            )
            assert found_number == str(invoice_number)
