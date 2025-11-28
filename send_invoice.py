#!/usr/bin/env python
# flake8: noqa: E402

from utils.platform_tools import ensure_python3

ensure_python3()

import os
import sys

from config.config import Configuration
from utils import exit_tools, input_tools

from billing import billing_tools
from mail import email


def main():
    print("E-mailer for invoices")

    # Get invoice number
    invoice_number = input_tools.input_integer(
        "Choose invoice number", billing_tools.get_latest_invoice_nr()
    )

    # Check that the invoice files exists
    invoices_path = billing_tools.get_invoice_path_from_nr(invoice_number)
    if invoices_path is None:
        exit_tools.paused_exit(f"Could not find invoice {invoice_number}")
    elif Configuration.instance().mailing.send_pdf:
        pdf_path = invoices_path.replace(".xlsx", ".pdf")
        if not os.path.exists(pdf_path):
            exit_tools.paused_exit(f"Could not find PDF file '{pdf_path}'")

    # Send the invoice email
    invoice_email = email.Email(
        recipient=Configuration.instance().mailing.invoice_recipient,
        subject_text=Configuration.instance().mailing.invoice_subject,
        body_text=Configuration.instance().mailing.invoice_body,
        cc_recipient=Configuration.instance().mailing.invoice_cc,
        attachment_path=invoices_path,
    )

    if not invoice_email.send():
        exit_tools.paused_exit("Could not send Excel invoice email")

    # Optionally send the PDF as well
    if Configuration.instance().mailing.send_pdf:
        pdf_email = email.Email(
            recipient=Configuration.instance().mailing.pdf_recipient,
            subject_text=Configuration.instance().mailing.pdf_subject,
            body_text=Configuration.instance().mailing.pdf_body,
            cc_recipient=None,
            attachment_path=pdf_path,
        )
        if not pdf_email.send():
            exit_tools.paused_exit("Could not send PDF invoice email")

    exit_tools.paused_exit("Invoices sent!")


if __name__ == "__main__":
    sys.excepthook = exit_tools.ows_abort_handler
    main()
