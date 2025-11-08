def paused_exit(message, exit_message="Press Enter to quit..."):
    """Pause the exit to allow user to read the message."""
    print(message)
    input(exit_message)
    exit(1)


def ows_abort_handler(exc_type, exc_value, exc_traceback):
    """Handle unhandled exceptions and pause the exit to allow user to read the error."""
    paused_exit(f"Aborted due to error: {exc_value}")


if __name__ == "__main__":
    paused_exit("This is a support module and should not be run directly")
