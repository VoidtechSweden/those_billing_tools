from datetime import date
from config.pattern_modules.pattern_module import PatternModule, register_pattern_module

@register_pattern_module
class YearPattern(PatternModule):
    
    def match(self):
        return r'\b\d{4}\b' # Four numbers only

    @classmethod
    def name(cls):
        return "year"

    def to_string(self):
        return date.today().year.__str__()

    def is_mandatory(self):
        return False