# Configuration Fields Description

This document describes all configuration fields used in the application.

## `[identification]`
- **name**: Your personal or sender's name.
- **company**: The company name associated with the billing.
- **email**: Email address used for identification and sending invoices.

## `[billing]`
- **invoices_path**: Directory path where invoice files are stored. All subdirectories are recursively searched.
- **invoice_pattern**: Pattern for invoice filenames, supporting placeholders like `{number}` and `{company}`. See the [Placeholders](#placeholders) section below.
- **template_path**: Directory path for invoice templates. No recursive search is used here.
- **template_prefix**: Prefix used to identify invoice template files.
- **create_pdf**: Boolean (`True`/`False`) to enable PDF creation for invoices.
- **pdf_converter**: Path to the PDF conversion executable (e.g., soffice from LibreOffice). 

## `[mailing]`
- **invoice_recipient**: Primary email address to send Excel invoices to.
- **invoice_cc**: Email address to receive a copy (CC) of the Excel invoice.
- **send_pdf**: Boolean (`True`/`False`) to enable sending PDF invoices too.
- **pdf_recipient**: Email address to receive the PDF version of the invoice.
> **Note:** Your own email address (from the `[identification]` section) will always be added as a BCC recipient when invoices are sent.

## `[mailing.smtp]`
- **port**: SMTP server port for sending emails.
- **server**: SMTP server address.
- **username**: Username for SMTP authentication.

## `[DEBUG]`
- **mail_to_self_only**: Boolean (`True`/`False`) to restrict email sending to the sender only, useful for testing.

## Placeholders

Placeholders are special tokens used in configuration fields to dynamically insert values. Some placeholders can accept parameters by adding a colon (`:`) and the parameter after the placeholder name. These placeholders are supported:

- `{number}`: Inserts the invoice number when later entered.
- `{currentdir}`: Inserts the current working directory path.
- `{company}`: Inserts the company name from the `[identification]` section.
- `{email}`: Inserts the email address from the `[identification]` section.
- `{name}`: Inserts the personal or sender's name from the `[identification]` section.
- `{date}`: Inserts the current date in the format `YYYY-MM-DD`.
- `{year}`: Inserts the current year.
- `{month}`: Inserts the current month in a human-readable format.  (e.g., "Januari")
    - Parameters:  
        - `swe`: Inserts the month name in Swedish. (Default)
        - `eng`: Inserts the month name in English.


### Invoice pattern placeholders

Placeholders in invoice_pattern are used to generically match file name patterns. For example, you can use placeholders to represent any year, date, number, or other variable parts of a file name. This allows flexible matching, such as recognizing files like 2025-MyCompany-invoice-23.xlsx by specifying the pattern like {year}-{company}-invoice-{number}.pdf.

