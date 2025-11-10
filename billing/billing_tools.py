import os
import re

from utils import exit_tools, input_tools

from config.config import Configuration

BILL_FILE_TYPE = ".xlsx"


def __find_all_invoices():

    # find all .xlsx files in all subdirectories that match the invoice pattern

    invoice_files = []
    invoice_regexp = Configuration.instance().billing.invoice_pattern.get_regexp()

    # check if invoice directory exists
    invoices_path = Configuration.instance().billing.invoice_path
    if not os.path.exists(invoices_path):
        assert False, f"Invoice directory does not exist: {invoices_path}"

    for root, dirs, files in os.walk(invoices_path):
        for file in files:
            if file.endswith(BILL_FILE_TYPE):
                if re.match(invoice_regexp, file):
                    invoice_files.append(os.path.join(root, file))
    return invoice_files


def invoice_already_exists(invoice_number):
    """
    Check if an invoice with the given number already exists in any year folder
    """
    return invoice_number in get_all_existing_invoice_numbers()


def get_all_existing_invoice_numbers():
    """
    Look in all subdirectories for existing invoices and return a list of all invoice numbers found
    """

    invoice_files = __find_all_invoices()

    bill_numbers = []
    for invoice_file in invoice_files:
        try:
            bill_number = int(
                Configuration.instance().billing.invoice_pattern.find_substitution_value(
                    "number", os.path.basename(invoice_file)
                )
            )
            bill_numbers.append(bill_number)
        except (IndexError, ValueError):
            continue

    return bill_numbers


def get_latest_invoice_nr():
    """
    Look in the latest year directory for existing invoices and find the last invoice number
    """
    invoice_numbers = get_all_existing_invoice_numbers()
    if invoice_numbers:
        return max(invoice_numbers)
    return 0


def get_invoice_path_from_nr(invoice_number):
    """
    Given a invoice number, return the path to the invoice file if it exists
    otherwise return None
    """

    invoice_name = create_invoice_name(invoice_number)

    invoice_files = __find_all_invoices()
    for invoice_file in invoice_files:
        if os.path.basename(invoice_file) == invoice_name:
            return invoice_file

    return None


def create_invoice_name(invoice_number):
    """
    Create a invoice name from the invoice number
    """
    invoice_pattern = Configuration.instance().billing.invoice_pattern
    return invoice_pattern.to_string_with_number(invoice_number) + BILL_FILE_TYPE


def create_invoice_path(invoice_number):
    """
    Create the full path for the invoice file based on where the last invoice was saved
    """

    invoice_name = create_invoice_name(invoice_number)

    last_invoice = get_latest_invoice_nr()
    last_invoice_file = get_invoice_path_from_nr(last_invoice)

    return os.path.join(
        (
            os.path.dirname(last_invoice_file)
            if last_invoice_file
            else Configuration.instance().billing.invoice_path
        ),
        invoice_name,
    )


def get_invoice_template_file():
    """
    Get the billing template file to use
    """
    template_prefix = Configuration.instance().billing.template_prefix
    template_path = Configuration.instance().billing.template_path
    template_files = [
        os.path.join(template_path, f)
        for f in os.listdir(template_path)
        if os.path.isfile(os.path.join(template_path, f))
        and f.startswith(template_prefix)
        and f.endswith(".xlsx")
    ]
    if not template_files:
        exit_tools.paused_exit(
            f"No template file with prefix '{template_prefix}' found in '{template_path}'"
        )
    elif len(template_files) == 1:
        template_file = template_files[0]
    else:
        template_file, index = input_tools.select_indexed_item(
            "Select a billing template", template_files
        )
    return template_file


if __name__ == "__main__":
    exit_tools.paused_exit("This is a support module and should not be run directly")
