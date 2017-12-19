from django.db import models


DIRECTION_CHOICES = (
    ('FWD', 'Forward'),
    ('REV', 'Reverse'),
)

ROLE_CHOICES = (
    ('PA', 'Pre-Amp'),
    ('ID', 'Identification'),
)

CONC_UNITS_CHOICES = (
    ('X', 'X'),
    ('mM', 'mM'),
    ('mg/ml', 'mg/ml'),
    ('mM each', 'mM each'),
    ('microM each', 'microM each'),
    ('ng/ul', 'ng/ul'),
    ('cp/ul', 'cp/ul'),
    ('%', '%'),
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


class Organism(models.Model):
    abbreviation = models.CharField(
            max_length=8, primary_key=True, unique=True)
    full_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return '%s:%s' % (self.abbreviation, self.full_name)


class Arg(models.Model):
    name = models.CharField(
            max_length=8, primary_key=True, unique=True)


class Strain(models.Model):
    name = models.CharField(
            max_length=20, primary_key=True, unique=True)
    organism = models.ForeignKey(
        Organism, related_name='strain', on_delete=models.PROTECT)
    arg = models.ForeignKey(
        Arg, related_name='Arg', on_delete=models.PROTECT)
    genome_size = models.BigIntegerField()


class CyclingPattern(models.Model):
    pattern_name = models.CharField(
            max_length=80, primary_key=True, unique=True)
    activation_time = models.PositiveIntegerField()
    activation_temp = models.PositiveIntegerField()
    num_cycles = models.PositiveIntegerField()
    denature_temp = models.PositiveIntegerField()
    denature_time = models.PositiveIntegerField()
    anneal_temp = models.PositiveIntegerField()
    anneal_time = models.PositiveIntegerField()
    extend_temp = models.PositiveIntegerField()
    extend_time = models.PositiveIntegerField()


class Concentration(models.Model):
    stock = models.DecimalField(max_digits=8, decimal_places=2)
    final = models.DecimalField(max_digits=8, decimal_places=2)
    units = models.CharField(max_length=15, choices=CONC_UNITS_CHOICES)

    def __str__(self):
        return '%.2f->%.2f->%s' % (self.stock, self.final, self.units)
