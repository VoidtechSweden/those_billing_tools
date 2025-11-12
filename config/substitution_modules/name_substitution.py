from config.config import Configuration
from config.substitution_modules.substitution_module import (
    SubstitutionModule,
    register_substitution_module,
)


@register_substitution_module
class NameSubstitution(SubstitutionModule):

    def match(self) -> str:
        return f"{Configuration.instance().identification.name}"

    @classmethod
    def name(cls) -> str:
        return "name"

    def to_string(self) -> str:
        return Configuration.instance().identification.name
