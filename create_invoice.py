#!/usr/bin/env python
# flake8: noqa: E402
from utils.platform_tools import ensure_python3

ensure_python3()

from billing.fields.invoice_date_field import InvoiceDateField
from billing.fields.invoice_number_field import InvoiceNumberField
from billing.fields.item_fields_generator import ItemFieldsGenerator
from billing.fields.month_period_field import MonthPeriodField
from billing.invoice import Invoice
from utils import exit_tools

from billing import billing_tools

from config.config import Configuration

import sys


def main():
    print(f"Creating invoice for {Configuration.instance().identification.company}")

    # Get the correct template to use
    template_file: str = billing_tools.get_invoice_template_file()
    print(f"Using billing template: '{template_file}'")
    invoice = Invoice(template_file)

    # Get invoice date
    date_field = InvoiceDateField()
    invoice.add_field(date_field)
    month_field = MonthPeriodField(date_field.get_date())
    invoice.add_field(month_field)
    print("Billing period: " + month_field.get_value())

    # Get new invoice number
    invoice_number_field = InvoiceNumberField()
    invoice_number = invoice_number_field.get_value()
    invoice.set_invoice_number(invoice_number)
    invoice.add_field(invoice_number_field)

    if billing_tools.invoice_already_exists(invoice_number):
        exit_tools.paused_exit(
            f"Invoice with number {invoice_number} already exists",
            "Exiting to avoid overwriting an existing file.",
        )

    # Generate the fields for billing hours or other items
    invoice.add_fields(ItemFieldsGenerator.generate_item_fields(template_file))

    # Create and save the invoices
    invoice.write_invoice()
    invoice.print_summary()

    exit_tools.paused_exit("Invoice created")


if __name__ == "__main__":
    sys.excepthook = exit_tools.ows_abort_handler
    main()
