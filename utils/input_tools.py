import datetime

from utils import basic_tools

def input_password(prompt):
    """
    Prompt the user for a password (input hidden)
    """
    import getpass

    while True:
        password = getpass.getpass(f"{prompt}: ")
        if password:
            return password
        else:
            print("Password can not be empty.")

def input_number(prompt, default=None):
    """
    Prompt the user for a number, with a default value
    """
    while True:
        if default is None:
            user_input = input(f"{prompt}: ")
        else:
            user_input = input(f"{prompt} [{default}]: ")
        if default is not None and user_input == "":
            return default
        try:
            value = int(user_input)
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")


def input_date(prompt, default):
    """
    Prompt the user for a date in YYYY-MM-DD format, with a default value
    """

    while True:
        user_input = input(f"{prompt} [{default.strftime('%Y-%m-%d')}]: ")
        if user_input == "":
            return default
        try:
            date = datetime.strptime(user_input, "%Y-%m-%d")
            return date
        except ValueError:
            print("Invalid date format. Please enter a date in the format YYYY-MM-DD.")


def select_indexed_item(prompt, items):
    """
    Prompt the user to select an item from a list by index
    """
    if not items:
        print("No items to choose from.")
        return None
    print(f"{prompt}:")
    for idx, item in enumerate(items):
        print(f"{idx + 1}: {item}")
    while True:
        user_input = input(f"Enter a number between 1 and {len(items)}: ")
        try:
            index = int(user_input)
            if 1 <= index <= len(items):
                return items[index - 1]
        except ValueError:
            print("Invalid input.")


if __name__ == "__main__":
    basic_tools.paused_exit("This is a support module and should not be run directly")
