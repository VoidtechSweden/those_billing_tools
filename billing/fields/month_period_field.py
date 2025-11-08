from billing.fields.invoice_field import InvoiceField


class MonthPeriodField(InvoiceField):
    """Class for invoice month period field"""

    def __init__(self, date):
        self.__date = date
        self.__month_period = ""
        super().__init__()

    def _month_to_shortstring(self, month):
        month_map = {
            1: "JAN",
            2: "FEB",
            3: "MARS",
            4: "APRIL",
            5: "MAJ",
            6: "JUNI",
            7: "JULI",
            8: "AUG",
            9: "SEPT",
            10: "OKT",
            11: "NOV",
            12: "DEC",
        }
        return month_map.get(month, "")

    def get_value(self):
        return self.__month_period

    def get_field(self):
        return "G19"

    def _process_value(self):
        self.__month_period = self._month_to_shortstring(self.__date.month)

    def get_description(self):
        return "Billing period"
