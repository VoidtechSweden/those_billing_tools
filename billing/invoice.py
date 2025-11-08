from billing import billing_tools
from config.config import Configuration
from utils import import_tools

import os

openpyxl = import_tools.try_import("openpyxl")


class Invoice:
    """Invoice to change invoice fields and write to file"""

    def __init__(self):
        self._invoice_fields = []
        self._template_file = None
        self._invoice_number = 0
        self._invoice_path = None

    def add_field(self, field):
        """
        Add an invoice field to be written
        """
        self._invoice_fields.append(field)

    def set_template_file(self, template_file):
        """
        Set the template file to be used
        """
        self._template_file = template_file

    def set_invoice_number(self, invoice_number):
        """
        Set the invoice number
        """
        self._invoice_number = invoice_number
        self._invoice_path = billing_tools.create_invoice_path(invoice_number)
        print(f"Invoice will be saved as: '{self._invoice_path}'")

    def write_invoice(self):
        """
        Write the invoice to the specified path
        """

        assert self._template_file is not None, "Template file not set"
        assert self._invoice_number != 0, "Invoice number not set"
        assert self._invoice_path is not None, "Invoice path not set"

        wb = openpyxl.load_workbook(self._template_file)
        ws = wb.active

        # Write all fields
        for field in self._invoice_fields:
            ws[field.get_field()] = field.get_value()

        wb.save(self._invoice_path)

        if Configuration.getboolean("billing", "create_pdf"):
            self._pdf_path = billing_tools.convert_to_pdf(self._invoice_path)

    def print_summary(self):
        print("\nInvoice summary")
        print("================================")
        print(f"Template: '{os.path.relpath(self._template_file)}'")
        for field in self._invoice_fields:
            print(f"{field.get_description()}: {field.get_value()}")
        print(f"XLSX: {os.path.relpath(self._invoice_path)}")
        print(f"PDF: {os.path.relpath(self._pdf_path) if self._pdf_path else 'NO'}")
        print("================================")
