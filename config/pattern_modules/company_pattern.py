from config.config import Configuration
from config.pattern_modules.pattern_module import PatternModule, register_pattern_module

@register_pattern_module
class CompanyPattern(PatternModule):
    
    def match(self):
        return Configuration.get('billing', 'company')

    @classmethod
    def name(cls):
        return "company"

    def to_string(self):
        return Configuration.get('billing', 'company')

    def is_mandatory(self):
        return False