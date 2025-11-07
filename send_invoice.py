import os

from config.config import Configuration
from utils import basic_tools, input_tools

from billing import billing_tools
from mail import mail_tools

BILL_EMAIL_INFO = mail_tools.EmailInfo(
    recipient=Configuration.get("mail", "invoice_recipient"),
    subject_text=f"{Configuration.get('billing', 'company')} faktura",
    body_text=f"Hej!\n\nBifogar månadens faktura för {Configuration.get('billing', 'company')}.\n\nMvh {Configuration.get('billing', 'name')}",
    cc_recipient=Configuration.get("mail", "invoice_cc"),
)

PDF_EMAIL_INFO = mail_tools.EmailInfo(
    recipient=Configuration.get("mail", "pdf_recipient"),
    subject_text=f"{Configuration.get('billing', 'company')}, utgående faktura",
    body_text="",
)


def main():
    print("E-mailer for invoices")

    # Get invoice number
    invoice_number = input_tools.input_number(
        "Choose invoice number", billing_tools.get_latest_invoice_nr()
    )

    # Check that the invoice files exists
    invoice_path = billing_tools.get_invoice_path_from_nr(invoice_number)
    if not invoice_path:
        basic_tools.paused_exit(f"Could not find invoice {invoice_number}")
    if Configuration.get("mail", "send_pdf"):
        pdf_path = invoice_path.replace(".xlsx", ".pdf")
        if not os.path.exists(pdf_path):
            basic_tools.paused_exit(f"Could not find PDF file '{pdf_path}'")

    # Send the invoice emails
    if not mail_tools.send_email(BILL_EMAIL_INFO, attachment_path=invoice_path):
        basic_tools.paused_exit("Could not send Excel invoice email")
    if Configuration.get("mail", "send_pdf"):
        if not mail_tools.send_email(PDF_EMAIL_INFO, attachment_path=pdf_path):
            basic_tools.paused_exit("Could not send PDF invoice email")

    basic_tools.paused_exit("Invoices sent!")


if __name__ == "__main__":
    main()
