from abc import abstractmethod
from abc import ABC
import glob
import importlib
import os


def register_substitution_module(cls):
    SubstitutionModuleRegistry.register(cls)
    return cls


class SubstitutionModule(ABC):

    @abstractmethod
    def match(self) -> str:
        """The pattern to match"""
        assert False, "You must implement match() method"

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """The name of the pattern"""
        assert False, "You must implement name() method"

    @abstractmethod
    def to_string(self) -> str:
        """The output string for the pattern"""
        assert False, "You must implement to_string() method"


class SubstitutionModuleRegistry:
    _substitution_registry: list[type[SubstitutionModule]] = []

    @classmethod
    def register(cls, substitution_module_class: type[SubstitutionModule]) -> None:
        cls._substitution_registry.append(substitution_module_class)

    @classmethod
    def _load_modules(cls) -> None:
        current_dir = os.path.dirname(os.path.relpath(__file__))
        substitution_files = glob.glob(os.path.join(current_dir, "*_substitution.py"))
        for substitution_file in substitution_files:
            module_name = (
                substitution_file.replace("/", ".")
                .replace("\\", ".")
                .replace(".py", "")
            )
            importlib.import_module(module_name)

    @classmethod
    def get_registered_modules(cls) -> list[type[SubstitutionModule]]:
        if len(cls._substitution_registry) == 0:
            cls._load_modules()
        return cls._substitution_registry
