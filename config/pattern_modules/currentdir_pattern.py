import os
import re
from config.config import Configuration
from config.pattern_modules.pattern_module import PatternModule, register_pattern_module

@register_pattern_module
class CurrentDirPattern(PatternModule):
    
    def match(self):
        assert False, "CurrentDirPattern does not support matching"

    @classmethod
    def name(cls):
        return "currentdir"

    def to_string(self):
        return os.getcwd()

    def is_mandatory(self):
        return False