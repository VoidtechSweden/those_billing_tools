from billing.fields.invoice_date_field import InvoiceDateField
from billing.fields.invoice_number_field import InvoiceNumberField
from billing.fields.month_period_field import MonthPeriodField
from billing.fields.normal_hours_field import NormalHoursField
from billing.invoice import Invoice
from utils import basic_tools

from billing import billing_tools

from config.config import Configuration

if __name__ == "__main__":

    print(f"Creating invoice for {Configuration.get('billing', 'company')}")

    invoice = Invoice()

    # Get invoice date
    date_field = InvoiceDateField()
    invoice.add_field(date_field)
    month_field = MonthPeriodField(date_field.get_date())
    invoice.add_field(month_field)
    print("Billing period: " + month_field.get_value())

    # Get normal hours
    invoice.add_field(NormalHoursField())

    # Get new invoice number
    invoice_number_field = InvoiceNumberField()
    invoice_number = invoice_number_field.get_value()
    invoice.set_invoice_number(invoice_number)
    invoice.add_field(invoice_number_field)

    if billing_tools.invoice_already_exists(invoice_number):
        basic_tools.paused_exit(
            f"Invoice with number {invoice_number} already exists",
            "Exiting to avoid overwriting an existing file.",
        )

    # Get the correct template to use
    template_file = billing_tools.get_invoice_template_file()
    print(f"Using billing template: '{template_file}'")
    invoice.set_template_file(template_file)

    # Create and save the invoices
    invoice.write_invoice()
    invoice.print_summary()

    basic_tools.paused_exit("Invoice created")
