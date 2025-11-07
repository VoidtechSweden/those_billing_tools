from billing import billing_tools
from billing.fields.invoice_field import InvoiceField


class MonthPeriodField(InvoiceField):
    """Class for invoice month period field"""

    def __init__(self, date):
        self.__date = date
        self.__month_period = ""
        super().__init__()

    def get_value(self):
        return self.__month_period

    def get_field(self):
        return "G19"

    def _process_value(self):
        self.__month_period = billing_tools.month_to_shortstring(self.__date.month)

    def get_description(self):
        return "Billing period"
