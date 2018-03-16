from django.db import models


class RuleScript(models.Model):
    """
    Little more than a big fat string. Holds the rules script as plan text.
    """
    text = models.TextField()

    @classmethod
    def make(cls, text):
        return RuleScript.objects.create(text = text)

    @classmethod
    def clone(cls,src):
        return cls.make(src.text)
