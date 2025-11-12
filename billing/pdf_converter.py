import os
import subprocess

from config.config import Configuration


class InvoicePdfConverter:

    @staticmethod
    def __get_expected_executable_name() -> str:
        if os.name == "nt":
            return "soffice.exe"
        else:
            return "soffice"

    @staticmethod
    def convert_invoice(invoice_path) -> str | None:
        """
        Convert the given excel invoice file to PDF using LibreOffice if installed
        Returns the path to the PDF file, or None if conversion failed
        """
        if not os.path.exists(invoice_path):
            print(
                f"Cannot create PDF. The invoice file '{invoice_path}' does not exist."
            )
            return None

        pdf_converter = Configuration.instance().billing.pdf_converter
        if not pdf_converter.endswith(
            InvoicePdfConverter.__get_expected_executable_name()
        ):
            print(
                f"Cannot create PDF. Specified PDF converter {pdf_converter} is not a {InvoicePdfConverter.__get_expected_executable_name()}"
            )

        if os.path.exists(pdf_converter):
            proposed_pdf_path = invoice_path.replace(".xlsx", ".pdf")
            print(
                "LibreOffice executable found. Creating PDF version of the invoice..."
            )
            result = subprocess.run(
                [
                    pdf_converter,
                    "--headless",
                    "--convert-to",
                    'pdf:calc_pdf_Export:{"PageRange":{"type":"string","value":"1"},"ExportNotes":{"type":"boolean","value":false}}',
                    invoice_path,
                    "--outdir",
                    os.path.dirname(invoice_path),
                ],
                capture_output=True,
                text=True,
            )
            print("----LibreOffice output:----")
            print(result.stdout)
            print(result.stderr)
            print("---------------------------")

            if result.returncode != 0:
                print("Could not convert to PDF. LibreOffice returned an error.")
                return None

            # Wait until file is created or timeout after 20 seconds
            import time

            start_time = time.time()
            while time.time() - start_time < 20:
                if os.path.exists(proposed_pdf_path):
                    print(f"PDF created: '{proposed_pdf_path}'")
                    return proposed_pdf_path

                time.sleep(1)
            if not os.path.exists(proposed_pdf_path):
                print(
                    "Could not create PDF. Timed out waiting for LibreOffice to create the file."
                )
        else:
            print("Cannot create PDF. LibreOffice is not found at the specified path.")

        return None
