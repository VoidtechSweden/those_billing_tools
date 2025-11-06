
from abc import abstractmethod
from abc import ABC
import glob
import importlib
import os

def register_pattern_module(cls):
    PatternModuleRegistry.register(cls)
    return cls

class PatternModuleRegistry:
    _registry = []

    @classmethod
    def register(cls, pattern_module_class):
        cls._registry.append(pattern_module_class)

    @classmethod
    def _load_modules(cls):
        current_dir = os.path.dirname(os.path.relpath(__file__))
        pattern_files = glob.glob(os.path.join(current_dir, "*_pattern.py"))
        for pattern_file in pattern_files:
            module_name = pattern_file.replace("/", ".").replace("\\", ".").replace(".py", "")
            importlib.import_module(module_name)

    @classmethod
    def get_registered_modules(cls):
        if len(cls._registry) == 0:
            cls._load_modules()
        return cls._registry

class PatternModule(ABC):
    
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

    @abstractmethod
    def is_mandatory(self):
        """Whether this pattern is mandatory to find"""
        assert False, "You must implement is_mandatory() method"