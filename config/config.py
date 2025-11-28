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
    invoices_path: str
    invoice_pattern: ConfigPattern | None
    template_path: str
    template_prefix: str
    create_pdf: bool
    pdf_converter: str


@dataclass
class SmtpConfig:
    server: str
    port: int


@dataclass
class MailingConfig:
    invoice_recipient: str
    invoice_cc: str
    invoice_subject: str
    invoice_body: str
    send_pdf: bool
    pdf_recipient: str
    pdf_subject: str
    pdf_body: str
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

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True

    def reload_config_file(self, config_file=None) -> None:
        if config_file:
            self.config_file = config_file
        self._load()

    @classmethod
    def instance(cls, config_file="my.config"):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance.config_file = config_file
            cls._instance._load()
        return cls._instance

    def __populate_dataclasses_from_parser(
        self, parser: configparser.ConfigParser
    ) -> None:
        self.identification = IdentificationConfig(
            name=parser.get("identification", "name"),
            company=parser.get("identification", "company"),
            email=parser.get("identification", "email"),
        )
        self.billing = BillingConfig(
            invoices_path=parser.get("billing", "invoices_path"),
            invoice_pattern=None,  # to be set later
            template_path=parser.get("billing", "template_path"),
            template_prefix=parser.get("billing", "template_prefix"),
            create_pdf=parser.getboolean("billing", "create_pdf"),
            pdf_converter=parser.get("billing", "pdf_converter"),
        )
        self.mailing = MailingConfig(
            invoice_recipient=parser.get("mailing", "invoice_recipient"),
            invoice_cc=parser.get("mailing", "invoice_cc"),
            invoice_subject=parser.get("mailing", "invoice_subject"),
            invoice_body=parser.get("mailing", "invoice_body"),
            send_pdf=parser.getboolean("mailing", "send_pdf"),
            pdf_recipient=parser.get("mailing", "pdf_recipient"),
            pdf_subject=parser.get("mailing", "pdf_subject"),
            pdf_body=parser.get("mailing", "pdf_body"),
            smtp=SmtpConfig(
                server=parser.get("mailing.smtp", "server"),
                port=parser.getint("mailing.smtp", "port"),
            ),
        )
        self.debug = DebugConfig(
            mail_to_self_only=parser.getboolean("DEBUG", "mail_to_self_only"),
        )
        self.__custom_placeholders = (
            parser.items("placeholders") if parser.has_section("placeholders") else []
        )

    def _load(self) -> None:
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
        templateparser.read(template_file, encoding="utf-8")
        parser.read(self.config_file, encoding="utf-8")

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
                        invoice_pattern.create(value, self.__custom_placeholders)
                        if not invoice_pattern.contains_number():
                            assert (
                                False
                            ), "Invoice name pattern must contain a '{number}' substitution module"
                        self.billing.invoice_pattern = invoice_pattern
                    elif "{" in value and "}" in value:
                        replacement_pattern = ConfigPattern()
                        replacement_pattern.create(value, self.__custom_placeholders)
                        parser.set(section, option, replacement_pattern.to_string())
                        substitution_performed = True

            if not substitution_performed:
                break
