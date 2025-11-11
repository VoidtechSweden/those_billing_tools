# THoSE Billing TOols
Billing tools for THoSE consultants

## Features

- Generate Excel and PDF invoices for THoSE consultants based on invoice templates
- Send the Excel invoices to THoSE
- Send PDF invoices to your billing system

## Usage

### Requirements

1. Windows OS (For now)
2. Python 3.13 or later
3. openpyxl (install with pip install openpyxl, or run scripts within pipenv)
4. Libreoffice installed for PDF conversion

### Configuration

1. Copy `template.config` to `my.config`.
2. Open `my.config` and fill in your company details, billing information, and any required SMTP server settings.

For detailed description about each field in the config file, see [Configuration](./docs/Configuration.md).

### Creating an Invoice

1. Run `create_invoice.py` (Either by running from windows explorer, or from terminal)
2. Enter the prompted information, such as date, hours worked, bill number.
3. The tool will generate both XLSX and PDF versions of the invoice in the same directory as the last invoice

### Sending an Invoice

1. Run `send_invoice.py` (Either by running from windows explorer, or from terminal)
2. Select the invoice number you want to send.
3. The script will email the invoice to THoSE and optionally to your billing system, depending on your configuration.

### Tips

- Make sure your configuration file is up to date before generating invoices.
- If many template files are in the template directory, a choice will be offered of what template file to use

## Contribute
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Setup

1. Ensure `pip` is installed. 
2. Install `pipenv` using `pip install pipenv`.
3. Copy pre-commit hook from .scripts to .git/hooks

> **Note for Windows users:**  
You may need to run pip commands using `python -m pip install pipenv` instead of just `pip install pipenv`.

## License

MIT License

