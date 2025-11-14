# Configuration Fields Description

This document describes all configuration fields used in the application.

## `[identification]`
- **name**: Your personal or sender's name.
- **company**: The company name associated with the billing.
- **email**: Email address used for identification and sending invoices.

## `[billing]`
- **invoices_path**: Directory path where invoice files are stored. All subdirectories are recursively searched.
- **invoice_pattern**: Pattern for invoice filenames to find, and to use when creating a invoice. Supporting placeholders, see [Invoice pattern placeholders](#invoice-pattern-placeholders) section below.
- **template_path**: Directory path for invoice templates. No recursive search is used here.
- **template_prefix**: Prefix used to identify invoice template files.
- **create_pdf**: Boolean (`True`/`False`) to enable PDF creation for invoices.
- **pdf_converter**: Path to the PDF conversion executable (e.g., soffice from LibreOffice). 

## `[mailing]`
- **invoice_recipient**: Primary email address to send Excel invoices to.
- **invoice_cc**: Email address to receive a copy (CC) of the Excel invoice.
- **invoice_subject**: Subject line for the email when sending Excel invoices.
- **invoice_body**: Body text for the email when sending Excel invoices.
- **send_pdf**: Boolean (`True`/`False`) to enable sending PDF invoices in addition to Excel invoices.
- **pdf_recipient**: Email address to send the PDF version of the invoice to.
- **pdf_subject**: Subject line for the email when sending PDF invoices.
- **pdf_body**: Body text for the email when sending PDF invoices.
> **Note:** Your own email address (from the `[identification]` section) will always be added as a BCC recipient when invoices are sent.

## `[mailing.smtp]`
- **port**: SMTP server port for sending emails.
- **server**: SMTP server address.
- **username**: Username for SMTP authentication.

## `[DEBUG]`
- **mail_to_self_only**: Boolean (`True`/`False`) to restrict email sending to the sender only, useful for testing.

## Placeholders

Placeholders are special tokens used in configuration fields to dynamically insert values in the configuration.

| Static placeholders| Substitutes for value| 
|----------------|----------------------------------------------------|
| `{company}`    | Company name from `[identification]` section       |
| `{email}`      | Email address from `[identification]` section      |
| `{name}`       | Name from `[identification]` section               |

| Dynamic placeholders| Substitutes for value| 
|----------------|----------------------------------------------------|
| `{currentdir}` | The current working directory path                 |
| `{date}`       | Current date in `YYYY-MM-DD` format  (Using numbers)|
| `{year}`       | Current year (e.g., `2024`)                        |
| `{month}`      | Current month in human-readable format (e.g., "Januari") |

### Placeholder parameters
Some placeholders can accept parameters by adding a colon (`:`) and the parameter after the placeholder name. 

- `{month}`
    - **swe**: The month name in Swedish. `{month:swe}` → "Mars" 
    - **eng**: The month name in English  `{month:swe}` → "March" 


### Invoice pattern placeholders

Placeholders used in `invoice_pattern` are used to generically match file name patterns with a created regexp. For example, you can use placeholders to represent any year, date, number, or other variable parts of a file name. This allows flexible matching, for example by specifying the pattern like `{year} {company}-invoice_{number}`.
This pattern will match any filename like these:
- `2025 MyCompany-invoice_23.xlsx`
- `2024 MyCompany-invoice_11.xlsx`
- `2023 MyCompany-invoice_1.xlsx`

| Static placeholder| Matches statically against                |
|----------------|-----------------------------------------------------|
| `{company}`    | Company name from `[identification]` section |
| `{email}`      | Email address from `[identification]` section |
| `{name}`       | Name from `[identification]` section |

| Dynamic Placeholder| Matches dynamically against                |
|----------------|-----------------------------------------------------|
| `{number}`     | Any number of any length |
| `{date}`       | Any date in `YYYY-MM-DD` format (Using numbers) |
| `{year}`       | Any four number year (e.g., `2024`)|
| `{month}`      | Any month in human-readable format (e.g., "Januari") |

When the invoice is saved, `invoice_pattern` will be used to generate a filename using the substitutions listed in [Placeholders](#placeholders)

### Custom Static Placeholders

You can define your own custom static placeholders by adding a `[placeholders]` section to your configuration file. Each entry in this section should specify a placeholder name and its corresponding value. Custom placeholders can then be used in any field that supports placeholders, just like the built-in ones.

**Example:**
```ini
[placeholders]
project=MyProject
client_code=12345
```

In your configuration fields, you can then use `{project}` or `{client_code}` to insert these values.


