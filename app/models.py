from django.db import models

class Primer(models.Model):
    code = models.CharField(max_length=40, primary_key=True, unique=True)
