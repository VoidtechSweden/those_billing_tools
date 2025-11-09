import configparser
import os
from config.config_pattern import ConfigPattern

from dataclasses import dataclass


@dataclass
class IdentificationConfig:
    name: str
    company: str
    email: str


@dataclass
class BillingConfig:
    invoice_path: str
    invoice_pattern: ConfigPattern
    template_path: str
    template_prefix: str
    create_pdf: bool
    pdf_converter: str


@dataclass
class SmtpConfig:
    server: str
    port: int
    username: str


@dataclass
class MailingConfig:
    invoice_recipient: str
    invoice_cc: str
    send_pdf: bool
    pdf_recipient: str
    smtp: SmtpConfig


@dataclass
class DebugConfig:
    mail_to_self_only: bool


# Singleton implementation
class Configuration:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_file="my.config"):
        if getattr(self, "_initialized", False):
            return
        self.config_file = config_file
        self._load()
        self._initialized = True

    def reload_config_file(self, config_file=None):
        if config_file:
            self.config_file = config_file
        self._load()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __populate_dataclasses_from_parser(self, parser):
        self.identification = IdentificationConfig(
            name=parser.get("identification", "name"),
            company=parser.get("identification", "company"),
            email=parser.get("identification", "email"),
        )
        self.billing = BillingConfig(
            invoice_path=parser.get("billing", "invoices_path"),
            invoice_pattern=None,  # to be set later
            template_path=parser.get("billing", "template_path"),
            template_prefix=parser.get("billing", "template_prefix"),
            create_pdf=parser.getboolean("billing", "create_pdf"),
            pdf_converter=parser.get("billing", "pdf_converter"),
        )
        self.mailing = MailingConfig(
            invoice_recipient=parser.get("mailing", "invoice_recipient"),
            invoice_cc=parser.get("mailing", "invoice_cc"),
            send_pdf=parser.getboolean("mailing", "send_pdf"),
            pdf_recipient=parser.get("mailing", "pdf_recipient"),
            smtp=SmtpConfig(
                server=parser.get("mailing.smtp", "server"),
                port=parser.getint("mailing.smtp", "port"),
                username=parser.get("mailing.smtp", "username"),
            ),
        )
        self.debug = DebugConfig(
            mail_to_self_only=parser.getboolean("DEBUG", "mail_to_self_only"),
        )

    def _load(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(
                f"Configuration file '{self.config_file}' not found."
            )
        template_file = "template.config"
        if not os.path.exists(template_file):
            raise FileNotFoundError(
                f"Template configuration file '{template_file}' not found."
            )

        print(f"Loading configuration from '{self.config_file}'")
        parser = configparser.ConfigParser()
        templateparser = configparser.ConfigParser()
        templateparser.read(template_file)
        parser.read(self.config_file)

        # Validate config against template
        for section in templateparser.sections():
            for option in templateparser.options(section):
                if not parser.has_option(section, option):
                    assert (
                        False
                    ), f"Missing configuration from template: [{section}] [{option}]"

        # Load dataclasses and perform substitution until no substitution patterns are found
        while True:
            substitution_performed = False
            self.__populate_dataclasses_from_parser(parser)

            # Handle config values with substitute patterns
            invoice_pattern = ConfigPattern()
            for section in parser.sections():
                for option in parser.options(section):
                    value = parser.get(section, option)

                    if section == "billing" and option == "invoice_pattern":
                        # Special handling for invoice pattern because it will be used programmatically
                        invoice_pattern.create(value)
                        if not invoice_pattern.contains_number():
                            assert (
                                False
                            ), "Invoice name pattern must contain a '{number}' substitution module"
                        self.billing.invoice_pattern = invoice_pattern
                    elif "{" in value and "}" in value:
                        replacement_pattern = ConfigPattern()
                        replacement_pattern.create(value)
                        parser.set(section, option, replacement_pattern.to_string())
                        substitution_performed = True

            if not substitution_performed:
                break
