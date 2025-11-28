# THoSE Billing Tools
Billing tools for THoSE consultants

## Features

- Generate Excel and PDF invoices for THoSE consultants based on invoice templates
- Send the Excel invoices to THoSE
- Send PDF invoices to your billing system
- Supports Windows and Linux

## Not yet supported features

* MacOS support
* TLS settings for mail (Now forced STARTTLS)
* "Utlägg" field to enter price per expendature

## Usage

### Requirements

1. Windows or Linux
2. Python 3 or later
3. openpyxl for excel file manipulation (install with pip install openpyxl, or run scripts within pipenv)
4. For PDF conversion: Libreoffice installed
5. For E-Mailing: Access to an SMTP server (THoSE outlook will not work)

### Configuration

1. Copy `template.config` to `my.config`.
2. Open `my.config` and fill in your company details, billing information, invoice patterns, template paths, any required SMTP server settings, etc.

For detailed description about each field in the config file, see [Configuration](./docs/Configuration.md).

### Creating an Invoice

1. Run `create_invoice.py` (Either by running from explorer, or from terminal)
2. Enter the prompted information, such as date, hours worked, bill number etc.
3. The tool will generate both XLSX and PDF versions of the invoice in the same directory as the last found invoice, or as the template if no previous invoices found.

### Sending an Invoice

1. Make sure you have configured SMTP correctly in the config 
2. Run `send_invoice.py` (Either by running from explorer, or from terminal)
3. Select the invoice number you want to send.
4. The script will email the invoice to THoSE and optionally to your billing system, depending on your configuration.
> **Note**: Your own email will always get a bcc of the sent emails

### Tips

- Make sure your configuration file is up to date with the template config file before generating invoices.
- If many invoice template files are in the template directory, a choice will be offered of what template file to use

## Contribute
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Setup for development

1. Ensure `pip` is installed. 
2. Install `pipenv` using `pip install pipenv`.
3. Copy pre-commit hook from .scripts to .git/hooks

> **Note for Windows developers:**  
You may need to run pip commands using `python -m pip install pipenv` instead of just `pip install pipenv`.

## License

MIT License