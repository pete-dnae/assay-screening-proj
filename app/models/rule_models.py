"""
A group of closely related model classes, which taken together define the
reagent allocations for a Plate.
"""


import re

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxValueValidator

from .odds_and_ends_models import mk_choices

class RuleScript(models.Model):
    """
    Represents instructions given by users in plain text . Text stored here are properly validated,
    So that they can later be parsed into alloc rule object .
    """
    script = models.CharField(max_length=2000)

    @classmethod
    def make(cls,script):
        return RuleScript.objects.create(script = script)

    @classmethod
    def clone(cls,src):
        return cls.make(src.script)