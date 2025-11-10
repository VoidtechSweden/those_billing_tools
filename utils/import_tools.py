import importlib
from typing import Any

from utils.exit_tools import paused_exit


def try_import(module_name: str, package_name: str | None = None) -> Any:
    """
    Try to import a module, and provide a user-friendly error message if it fails
    """

    try:
        module = importlib.import_module(module_name, package_name)
        return module
    except ImportError:
        print(
            f"Error: Could not import module '{module_name}'. Try installing using pip install {package_name}"
        )
        paused_exit("Unresolvable dependency encountered")
        return None


if __name__ == "__main__":
    paused_exit("This is a support module and should not be run directly")
