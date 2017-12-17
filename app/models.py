from django.db import models


DIRECTION_CHOICES = (
    ('FWD', 'Forward'),
    ('REV', 'Reverse'),
)

ROLE_CHOICES = (
    ('PA', 'Pre-Amp'),
    ('ID', 'Identification'),
)


class Primer(models.Model):
    code = models.CharField(max_length=40, primary_key=True, unique=True)
    direction = models.CharField(max_length=7, choices=DIRECTION_CHOICES)


class PrimerPair(models.Model):
    fwd = models.ForeignKey(
        Primer, related_name='pair_fwd', on_delete=models.CASCADE)
    rev = models.ForeignKey(
        Primer, related_name='pair_rev', on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)

