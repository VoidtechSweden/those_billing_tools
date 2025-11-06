import os
import re
import re
import subprocess

from utils import basic_tools

from config.config import Configuration

SOFFICE_PATH = "C:\\Program Files\\LibreOffice\\program\\soffice.exe"

BILL_FILE_TYPE = ".xlsx"    

class BillFields:
    NUMBER_FIELD = "G18"
    MONTH_FIELD = "G19"
    DATE_FIELD = "G20"
    HOURS_FIELD = "C28"


def __find_all_invoices():

    #find all .xlsx files in all subdirectories that match the invoice pattern
    
    invoice_files = []
    invoice_regexp = Configuration.get_invoice_pattern().get_regexp()

    #check if invoice directory exists
    invoices_path = Configuration.get('billing', 'invoices_path')
    if not os.path.exists(invoices_path):
        assert False, f"Invoice directory does not exist: {invoices_path}"

    for root, dirs, files in os.walk(invoices_path):
        for file in files:
            if file.endswith(BILL_FILE_TYPE):
                if re.match(invoice_regexp, file):
                    invoice_files.append(os.path.join(root, file))
    return invoice_files

def invoice_already_exists(invoice_number):
    """
    Check if an invoice with the given number already exists in any year folder
    """
    return invoice_number in get_all_existing_invoice_numbers()


def get_all_existing_invoice_numbers():
    """
    Look in all subdirectories for existing invoices and return a list of all invoice numbers found
    """

    invoice_files = __find_all_invoices()

    bill_numbers = []
    for invoice_file in invoice_files:
        try:
            bill_number = int(Configuration.get_invoice_pattern().find_pattern("number", os.path.basename(invoice_file)))
            bill_numbers.append(bill_number)
        except (IndexError, ValueError):
            continue

    return bill_numbers


def get_latest_invoice_nr():
    """
    Look in the latest year directory for existing invoices and find the last invoice number
    """
    invoice_numbers = get_all_existing_invoice_numbers()
    if invoice_numbers:
        return max(invoice_numbers)
    return 0


def get_invoice_path_from_nr(invoice_number):
    """
    Given a invoice number, return the path to the invoice file if it exists
    otherwise return None
    """

    invoice_name = create_invoice_name(invoice_number)

    invoice_files = __find_all_invoices()
    for invoice_file in invoice_files:
        if os.path.basename(invoice_file) == invoice_name:
            return invoice_file
        
    return None


def create_invoice_name(invoice_number):
    """
    Create a invoice name from the invoice number
    """
    invoice_pattern = Configuration.get_invoice_pattern()
    return invoice_pattern.to_string_with_number(invoice_number) + BILL_FILE_TYPE

def create_invoice_path(invoice_number):
    """
    Create the full path for the invoice file based on where the last invoice was saved
    """

    invoice_name = create_invoice_name(invoice_number)
    last_invoice_file = get_invoice_path_from_nr(invoice_number - 1)

    return os.path.join(os.path.dirname(last_invoice_file) if last_invoice_file else Configuration.get('billing', 'invoices_path'), invoice_name)

def month_to_shortstring(month):
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


def convert_to_pdf(invoice_path):
    """
    Convert the given bill file to PDF using LibreOffice if installed
    Return the path to the PDF file or None if conversion failed
    """
    if not os.path.exists(invoice_path):
        print(f"Cannot create PDF. The file '{invoice_path}' does not exist.")
        return None

    pdf_path = None
    if os.path.exists(SOFFICE_PATH):
        proposed_pdf_path = invoice_path.replace(BILL_FILE_TYPE, ".pdf")
        print("LibreOffice is installed. Creating PDF version of the invoice...")
        result = subprocess.run(
            [
            SOFFICE_PATH,
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

        #Wait until file is created or timeout after 20 seconds
        import time
        start_time = time.time()
        while time.time() - start_time < 20:
            if os.path.exists(proposed_pdf_path):
                print(f"PDF created: '{proposed_pdf_path}'")
                pdf_path = proposed_pdf_path
                break
            time.sleep(1)
        if not os.path.exists(proposed_pdf_path):
            print("Could not create PDF. Timed out waiting for LibreOffice to create the file.")
    else:
        print(
            "Cannot create PDF. LibreOffice is not installed on this computer."
        )
    return pdf_path


if __name__ == "__main__":
    basic_tools.paused_exit("This is a support module and should not be run directly")
