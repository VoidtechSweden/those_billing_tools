from billing import billing_tools
from billing.fields.invoice_field import InvoiceField
from billing.pdf_converter import InvoicePdfConverter
from config.config import Configuration
from utils import import_tools
from billing.fields.item_fields_generator import ItemFieldsGenerator

import os

openpyxl = import_tools.try_import("openpyxl")

BILL_FILE_TYPE = ".xlsx"


class Invoice:
    """
    Invoice to change invoice fields in a template file and write to a new file
    """

    def __init__(self, template_file) -> None:
        self._invoice_fields: list[InvoiceField] = []
        self._template_file: str = template_file
        self._invoice_number: int = 0
        self._invoice_path: str = ""
        self._pdf_path: str = ""

    def add_field(self, field: InvoiceField) -> None:
        """
        Add an invoice field to be written
        """
        self._invoice_fields.append(field)

    def set_invoice_number(self, invoice_number: int) -> None:
        """
        Set the invoice number
        """
        self._invoice_number = invoice_number
        self._invoice_path = billing_tools.create_invoice_path(invoice_number)
        print(f"Invoice will be saved as: '{self._invoice_path}'")

    def generate_item_fields(self) -> None:
        """
        Generate the item fields for the invoice
        """

        generator = ItemFieldsGenerator(self._template_file)
        item_fields = generator.generate_item_fields()
        for field in item_fields:
            self.add_field(field)

    def write_invoice(self) -> None:
        """
        Write the invoice to the specified path
        """
        assert self._invoice_number != 0, "Invoice number not set"
        assert self._invoice_path != "", "Invoice path not set"

        wb = openpyxl.load_workbook(self._template_file)
        ws = wb.active

        # Write all fields
        for field in self._invoice_fields:
            ws[field.get_field()] = field.get_value()

        wb.save(self._invoice_path)

        if Configuration.instance().billing.create_pdf:
            pdf_path = InvoicePdfConverter.convert_invoice(self._invoice_path)
            if pdf_path is not None:
                self._pdf_path = pdf_path

    def print_summary(self):
        print("")
        print("================================")
        print("\nINVOICE SUMMARY")
        print("================================")
        print(f"Template: '{os.path.relpath(self._template_file)}'")
        for field in self._invoice_fields:
            print(f"{field.get_description()}: {field.get_value()}")
        print(f"XLSX: {os.path.relpath(self._invoice_path)}")
        print(
            f"PDF: {os.path.relpath(self._pdf_path) if self._pdf_path != '' else 'NO'}"
        )
        print("================================")
