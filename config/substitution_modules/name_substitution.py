from config.config import Configuration
from config.substitution_modules.substitution_module import (
    SubstitutionModule,
    register_substitution_module,
)


@register_substitution_module
class NameSubstitution(SubstitutionModule):

    def match(self):
        return Configuration.instance().identification.name

    @classmethod
    def name(cls):
        return "name"

    def to_string(self):
        return Configuration.instance().identification.name
