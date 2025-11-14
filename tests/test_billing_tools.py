import contextlib
import os
import shutil
import tempfile
from billing import billing_tools
from config.config import Configuration
from tests.conftest import temporary_config


@contextlib.contextmanager
def temporary_invoices(invoice_numbers: list[int]):
    """Create temporary invoices in a temp directory for testing purposes."""

    with tempfile.TemporaryDirectory(prefix="temp_invoices", delete=False) as temp_dir:
        print(f"Created temporary invoices directory at {temp_dir}")
        Configuration.instance().billing.invoices_path = temp_dir

        start_year = 2000
        invoice_per_year = 5

        for index, invoice_number in enumerate(invoice_numbers):
            # Create year subfolder
            if index % invoice_per_year == 0:
                year_dir = os.path.join(
                    temp_dir, str(start_year + index // invoice_per_year)
                )
                os.makedirs(year_dir, exist_ok=True)

            # Generate valid invoice names
            invoice_name = (
                Configuration.instance().billing.invoice_pattern.to_string_with_number(
                    invoice_number
                )
                + ".xlsx"
            )
            invoice_file_path = os.path.join(year_dir, invoice_name)

            with open(invoice_file_path, "w") as f:
                f.write("Test Invoice Content")

        yield temp_dir

    print(f"Removing temporary invoices directory at {temp_dir}")
    shutil.rmtree(temp_dir)


def test_invoice_numbers():
    """
    TEST: Getting all existing invoice numbers and the latest invoice number from a folder of valid invoices

    EXPECTED: Correct invoice numbers are returned
    """

    company = "TestCompany"
    invoice_pattern = "TestINVOICE {company} {date}_{number}"
    config_fields = [
        ("billing", "invoice_pattern", invoice_pattern),
        ("identification", "company", company),
    ]
    invoice_numbers = list(range(15, 51))

    with temporary_config(updated_fields=config_fields):
        with temporary_invoices(invoice_numbers) as invoices_path:
            assert billing_tools.get_all_existing_invoice_numbers() == list(
                invoice_numbers
            ), "Failed to get all existing invoice numbers"
            assert billing_tools.get_latest_invoice_nr() == max(
                invoice_numbers
            ), "Failed to get latest invoice number"
            assert (
                billing_tools.get_invoice_path_from_nr(max(invoice_numbers)) is not None
            ), "Failed to get invoice path for existing invoice number"
            assert (
                billing_tools.get_invoice_path_from_nr(max(invoice_numbers) + 1) is None
            ), "Incorrectly found invoice path for non-existing invoice number"
            assert (
                billing_tools.invoice_already_exists(max(invoice_numbers) - 5) is True
            ), "Failed to recognize existing invoice number"
            assert (
                billing_tools.invoice_already_exists(max(invoice_numbers) + 1) is False
            ), "Incorrectly recognized non-existing invoice number"
            new_invoice_path = billing_tools.create_invoice_path(
                max(invoice_numbers) + 1
            )
            assert invoices_path in os.path.dirname(
                new_invoice_path
            ), "Failed to create correct invoice path for new invoice number."
