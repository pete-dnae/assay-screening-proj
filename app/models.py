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
    string_code = models.CharField(
            max_length=40, primary_key=True, unique=True)
    direction = models.CharField(
            max_length=7, choices=DIRECTION_CHOICES)


class PrimerPair(models.Model):
    # Note the *string_code* primary key is synthesised automatically in the 
    # overidden save() method.
    string_code = models.CharField(
            primary_key=True, max_length=80, editable=False, unique=True)

    fwd_primer = models.ForeignKey(
        Primer, related_name='pair_fwd', on_delete=models.PROTECT)
    rev_primer = models.ForeignKey(
        Primer, related_name='pair_rev', on_delete=models.PROTECT)
    # For ID or PA?
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)



    """
    Override save(), in order to keep the string_code field in synch with
    the forward and reverse primers used.
    """
    def save(self, *args, **kwargs):
        self.string_code = '_X_'.join((
                self.fwd_primer.string_code, self.rev_primer.string_code))
        super().save(*args, **kwargs)
