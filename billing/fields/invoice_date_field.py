from datetime import datetime as DateTime
from billing.fields.invoice_field import InvoiceField
from utils import input_tools


class InvoiceDateField(InvoiceField):
    """Class for invoice date field"""

    def __init__(self):
        self.__invoice_date = None

        super().__init__()

    def get_date(self):
        return self.__invoice_date

    def get_value(self):
        return self.__invoice_date.strftime("%Y-%m-%d")

    def get_field(self):
        return "G20"

    def _process_value(self):
        self.__invoice_date = input_tools.input_date(
            "Enter date (YYYY-MM-DD)", DateTime.now()
        )

    def get_description(self):
        return "Invoice date"
