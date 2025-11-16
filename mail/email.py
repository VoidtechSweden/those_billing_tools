from email.utils import formatdate
from email.message import EmailMessage
import mimetypes
import os
import smtplib
from config.config import Configuration
from utils import input_tools


class server_settings:
    SMTP_SERVER = Configuration.instance().mailing.smtp.server
    SMTP_PORT = Configuration.instance().mailing.smtp.port
    SMTP_USER = Configuration.instance().mailing.smtp.username
    SMTP_PASSWORD = ""


class Email:
    """
    Class to create and send an email with optional attachment
    """

    def __init__(
        self,
        recipient,
        subject_text,
        body_text,
        cc_recipient=None,
        attachment_path=None,
    ) -> None:
        self.recipient: str = recipient
        self.subject_text: str = subject_text
        self.body_text: str = body_text
        self.cc_recipient: str | None = cc_recipient
        self.attachment_path: str | None = attachment_path

    def add_attachment(self, attachment_path: str) -> None:
        self.attachment_path = attachment_path

    def send(self) -> bool:
        """
        Send an email with an optional attachment
        return True if sent OK, False if failed
        """
        sent = False

        print("")
        print("================================")
        print("MAIL:")
        print("================================")
        if self.attachment_path is not None:
            print(f"FILE: {self.attachment_path}")
        print(f"FROM: <{Configuration.instance().identification.email}>")
        if Configuration.instance().debug.mail_to_self_only:
            print(
                f"TO:   <{Configuration.instance().identification.email}> (DEBUG MODE)"
            )
        else:
            print(f"TO:   <{self.recipient}>")
            if self.cc_recipient:
                print(f"CC:   <{self.cc_recipient}>")
        print(f"SUBJECT: '{self.subject_text}'")
        print(f"BODY:    '{self.body_text}'")
        print("================================")
        input("Press enter to send or ctrl-c to cancel.")

        # Create the container email message.
        msg = EmailMessage()
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = self.subject_text
        msg["From"] = Configuration.instance().identification.email
        if Configuration.instance().debug.mail_to_self_only:
            print(
                "DEBUG: Overriding recipient to send mail to self only (mail_to_self_only=True)"
            )
            msg["To"] = Configuration.instance().identification.email
        else:
            msg["To"] = self.recipient
            if self.cc_recipient:
                msg["Cc"] = self.cc_recipient

        msg.set_content(self.body_text)
        msg["Bcc"] = Configuration.instance().identification.email  # Bcc to self

        if self.attachment_path is not None:
            # Deduct mime type of the file
            mime_type, _ = mimetypes.guess_type(self.attachment_path)
            if mime_type is None:
                if self.attachment_path.endswith(".xlsx"):
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                elif self.attachment_path.endswith(".pdf"):
                    mime_type = "application/pdf"

            assert mime_type is not None, "Could not deduce mime type of attachment"
            mimetype_split = mime_type.split("/")

            with open(self.attachment_path, "rb") as fp:
                msg.add_attachment(
                    fp.read(),
                    maintype=mimetype_split[0],
                    subtype=mimetype_split[1],
                    filename=os.path.basename(self.attachment_path),
                )
        else:
            print("NOTE: E-mail has no attached file")

        # Send the email via the specified SMTP server using STARTTLS.
        try:

            print(
                f"Connecting to SMTP server {server_settings.SMTP_SERVER}:{server_settings.SMTP_PORT}"
            )

            with smtplib.SMTP(
                host=server_settings.SMTP_SERVER,
                port=server_settings.SMTP_PORT,
                timeout=20,
            ) as smtp_connection:
                print("Sending ehlo...")
                smtp_connection.ehlo()
                print("Starting TLS...")
                smtp_connection.starttls()
                if not server_settings.SMTP_PASSWORD:
                    server_settings.SMTP_PASSWORD = input_tools.input_password(
                        "Enter password to SMTP server"
                    )
                print("Logging in to SMTP server...")
                smtp_connection.login(
                    server_settings.SMTP_USER, server_settings.SMTP_PASSWORD
                )
                print("Sending e-mail...")
                response = smtp_connection.send_message(msg)
                if response:  # send_message returns a dictionary of failed recipients
                    print(f"Failed to send email: {response}")
                else:
                    print("Email sent successfully!")
                    sent = True
        except smtplib.SMTPException as e:
            print(f"Exception while sending email: {e}")
        except Exception as e:
            print(f"Unexpected exception: {e}")
        print("================================\n\n")

        return sent
