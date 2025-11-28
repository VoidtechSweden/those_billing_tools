def paused_exit(
    message: str, exit_message: str = "Press Enter to quit...", exit_code: int = 0
) -> None:
    """Pause the exit to allow user to read the message."""
    print(message)
    input(exit_message)
    exit(exit_code)


def ows_abort_handler(exc_type, exc_value, exc_traceback) -> None:
    """Handle unhandled exceptions and pause the exit to allow user to read the error."""
    # identify if used pressed ctrl+c
    if issubclass(exc_type, KeyboardInterrupt):
        paused_exit(message="Aborted by user", exit_code=1)
    else:
        paused_exit(message=f"Aborted due to error: {exc_value}", exit_code=1)


if __name__ == "__main__":
    paused_exit("This is a support module and should not be run directly")
