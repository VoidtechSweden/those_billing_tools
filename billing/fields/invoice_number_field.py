from billing import billing_tools
from billing.fields.invoice_field import InvoiceField
from utils import input_tools


class InvoiceNumberField(InvoiceField):
    """Class for invoice number fields"""

    def __init__(self) -> None:
        self.__invoice_number = 0

        super().__init__()

    def get_value(self) -> int:
        return self.__invoice_number

    def get_field(self) -> str:
        return "G18"

    def _process_value(self) -> None:
        self.__invoice_number = input_tools.input_number(
            "Enter invoice number", billing_tools.get_latest_invoice_nr() + 1
        )

    def get_description(self) -> str:
        return "Invoice number"
