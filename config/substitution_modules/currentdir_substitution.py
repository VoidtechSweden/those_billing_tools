import os
from config.substitution_modules.substitution_module import (
    SubstitutionModule,
    register_substitution_module,
)


@register_substitution_module
class CurrentDirSubstitution(SubstitutionModule):

    def match(self):
        assert False, "CurrentDirPattern does not support matching"

    @classmethod
    def name(cls):
        return "currentdir"

    def to_string(self):
        return os.getcwd()
