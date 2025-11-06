# those_billing_tools
Billing tools for THoSE consultants

## Features

- Generate xlsx and PDF invoices for THoSE consultants based on invoice templates
- Send the invoices to THoSE
- Send PDF invoices to your billing system

## Setup
TODO

## Configuration

1. Copy `template.config` to `my.config`.
2. Open `my.config` and fill in your company details, billing information, and any required SMTP server settings.

## Creating an Invoice

1. Run `create_invoice.py`.
2. Enter the prompted information, such as date, hours worked, bill number.
3. The tool will generate both XLSX and PDF versions of the invoice in the same directory as the last invoice

## Sending an Invoice

1. Run `send_invoice.py`.
2. Select the invoice number you want to send.
3. The script will email the invoice to THoSE and optionally to your billing system, depending on your configuration.

## Tips

- Make sure your configuration file is up to date before generating invoices.
- If many template files are in the template directory, a choice will be offered of what template file to use

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License

