from billing.fields.invoice_field import InvoiceField
from utils import input_tools


class BillableItemField(InvoiceField):
    """Class for invoice billable item field"""

    def __init__(self, field_number, item_description):
        self._field_number = field_number
        self._item_description = item_description
        self._billable_value: float = 0.0

        super().__init__()

    def get_value(self) -> float:
        return self._billable_value

    def get_field(self) -> str:
        return self._field_number

    def _process_value(self):
        self._billable_value = input_tools.input_number(
            f"Enter {self.get_description()}"
        )

    def get_description(self):
        return self._item_description
