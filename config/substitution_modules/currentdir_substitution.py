import os
from config.substitution_modules.substitution_module import (
    SubstitutionModule,
    register_substitution_module,
)


@register_substitution_module
class CurrentDirSubstitution(SubstitutionModule):

    def match(self) -> str:
        assert False, "CurrentDirPattern does not support matching"

    @classmethod
    def name(cls) -> str:
        return "currentdir"

    def to_string(self) -> str:
        return os.getcwd()
