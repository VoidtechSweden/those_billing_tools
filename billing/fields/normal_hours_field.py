from billing.fields.invoice_field import InvoiceField
from utils import input_tools


class NormalHoursField(InvoiceField):
    """Class for worked normal hours fields"""

    def __init__(self):
        self.__worked_hours: float = 0.0

        super().__init__()

    def get_value(self) -> float:
        return self.__worked_hours

    def get_field(self) -> str:
        return "C28"

    def _process_value(self):
        self.__worked_hours = input_tools.input_number("Enter worked (normal) hours")

    def get_description(self) -> str:
        return "Hours (normal)"
