import os
import smtplib
from email.message import EmailMessage
import mimetypes

from billing.billing_tools import BillInfo
from config.config import Configuration
from utils import basic_tools, input_tools


class server_settings:
    SMTP_SERVER = Configuration.get('mail', 'smtp_server')
    SMTP_PORT = Configuration.get('mail', 'smtp_port')
    SMTP_USER = Configuration.get('mail', 'smtp_user')
    SMTP_PASSWORD = ""


class EmailInfo:
    def __init__(self, recipient, subject_text, body_text, cc_recipient=None):
        self.recipient = recipient
        self.subject_text = subject_text
        self.body_text = body_text
        self.cc_recipient = cc_recipient


def send_email(email_info, attachment_path):
    """
    Send an email with the attachment
    return True if sent OK, False if failed
    """
    sent = False

    print(f"MAIL:")
    print("================================")
    if attachment_path is not None:
        print(f"FILE: {attachment_path}")
    print(f"FROM: <{server_settings.SMTP_USER}>")
    print(f"TO:   <{email_info.recipient}>")
    if email_info.cc_recipient:
        print(f"CC:   <{email_info.cc_recipient}>")
    print(f"SUBJECT: '{email_info.subject_text}'")
    print(f"BODY:    '{email_info.body_text}'")
    print("================================")
    input("Press enter to send or ctrl-c to cancel.")

    # Create the container email message.
    msg = EmailMessage()
    msg["Subject"] = email_info.subject_text
    msg["From"] = server_settings.SMTP_USER
    msg["To"] = email_info.recipient
    msg.set_content(email_info.body_text)
    if email_info.cc_recipient:
        msg["Cc"] = email_info.cc_recipient
    msg["Bcc"] = server_settings.SMTP_USER  # Bcc to self

    if attachment_path is not None:
        # Deduct mime type of the file
        mime_type, _ = mimetypes.guess_type(attachment_path)
        if mime_type is None:
            if attachment_path.endswith(".xlsx"):
                mime_type = (
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            elif attachment_path.endswith(".pdf"):
                mime_type = "application/pdf"

        with open(attachment_path, "rb") as fp:
            msg.add_attachment(
                fp.read(),
                maintype=mime_type.split("/")[0],
                subtype=mime_type.split("/")[1],
                filename=os.path.basename(attachment_path),
            )

    # Send the email via the specified SMTP server using STARTTLS.
    try:

        if not server_settings.SMTP_PASSWORD:
            server_settings.SMTP_PASSWORD = input_tools.input_password(f"Enter password to SMTP server")

        with smtplib.SMTP(
            server_settings.SMTP_SERVER, server_settings.SMTP_PORT
        ) as smtp_connection:
            smtp_connection.ehlo()
            smtp_connection.starttls()
            smtp_connection.login(
                server_settings.SMTP_USER, password
            )
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


if __name__ == "__main__":
    basic_tools.paused_exit("This is a support module and should not be run directly")
