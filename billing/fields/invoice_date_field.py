from datetime import datetime
from billing.fields.invoice_field import InvoiceField
from utils import input_tools


class InvoiceDateField(InvoiceField):
    """Class for invoice date field"""

    def __init__(self) -> None:
        self.__invoice_date: datetime | None = None

        super().__init__()

    def get_date(self) -> datetime | None:
        return self.__invoice_date

    def get_value(self) -> str:
        if self.__invoice_date is None:
            return ""
        else:
            return self.__invoice_date.strftime("%Y-%m-%d")

    def get_field(self) -> str:
        return "G20"

    def _process_value(self) -> None:
        self.__invoice_date = input_tools.input_date(
            "Enter date (YYYY-MM-DD)", datetime.now()
        )

    def get_description(self) -> str:
        return "Invoice date"
