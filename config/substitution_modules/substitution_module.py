from abc import abstractmethod
from abc import ABC
import glob
import importlib
import os


def register_substitution_module(cls):
    SubstitutionModuleRegistry.register(cls)
    return cls


class SubstitutionModuleRegistry:
    _registry = []

    @classmethod
    def register(cls, substitution_module_class):
        cls._registry.append(substitution_module_class)

    @classmethod
    def _load_modules(cls):
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
    def get_registered_modules(cls):
        if len(cls._registry) == 0:
            cls._load_modules()
        return cls._registry


class SubstitutionModule(ABC):

    @abstractmethod
    def match(self):
        """The pattern to match"""
        assert False, "You must implement match() method"

    @classmethod
    @abstractmethod
    def name(cls):
        """The name of the pattern"""
        assert False, "You must implement name() method"

    @abstractmethod
    def to_string(self):
        """The output string for the pattern"""
        assert False, "You must implement to_string() method"
