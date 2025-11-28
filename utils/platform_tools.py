import importlib
import os
import sys
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


def ensure_python3():
    """
    Ensure that the script is running under Python 3
    """
    if sys.version_info[0] < 3:
        python3 = "python3"
        if sys.platform == "win32":
            python3 = "py -3"
        # make sure paths are relative in argv
        sys.argv = [os.path.relpath(arg) for arg in sys.argv]
        os.execvp(python3.split()[0], python3.split() + sys.argv)


if __name__ == "__main__":
    paused_exit("This is a support module and should not be run directly")
