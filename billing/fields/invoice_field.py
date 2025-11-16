from abc import ABC, abstractmethod


class InvoiceField(ABC):
    """Base class for invoice fields"""

    def __init__(self) -> None:
        self._process_value()

    @abstractmethod
    def get_value(self) -> int | float | str:
        """Return the value for the field"""

        assert False, "You must implement get_value() method"

    @abstractmethod
    def get_field(self) -> str:
        """Return the name of the field"""
        assert False, "You must implement get_field() method"

    @abstractmethod
    def _process_value(self) -> None:
        """Get the value to be stored in the field"""

        assert False, "You must implement _process_value() method"

    @abstractmethod
    def get_description(self) -> str:
        """Return a description of the field"""
        assert False, "You must implement get_description() method"
