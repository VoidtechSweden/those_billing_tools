import base64


def decode_password(encoded):
    """
    Decode the SMTP password from a base64 encoded string
    This is just to avoid having the password in plain text in the code
    """
    return base64.b64decode(encoded).decode("utf-8")


def paused_exit(message, exit_message="Press Enter to quit..."):
    print(message)
    input(exit_message)
    exit(1)


if __name__ == "__main__":
    paused_exit("This is a support module and should not be run directly")
