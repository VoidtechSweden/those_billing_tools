from config.config import Configuration
from config.substitution_modules.substitution_module import (
    SubstitutionModule,
    register_substitution_module,
)


@register_substitution_module
class CompanySubstitution(SubstitutionModule):

    def match(self):
        return Configuration.instance().identification.company

    @classmethod
    def name(cls):
        return "company"

    def to_string(self):
        return Configuration.instance().identification.company
