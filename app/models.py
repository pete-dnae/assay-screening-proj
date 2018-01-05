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

PLACEHOLDER_CHOICES = (
    ('Primers', 'Primers'),
    ('Template', 'Template'),
    ('HgDNA', 'HgDNA')
)

PRIMER_ROLE_CHOICES = (
    ('fwd', 'forward'),
    ('rev', 'reverse'),
)


class Concentration(models.Model):
    stock = models.DecimalField(max_digits=8, decimal_places=2)
    final = models.DecimalField(max_digits=8, decimal_places=2)
    units = models.CharField(max_length=15, choices=CONC_UNITS_CHOICES)


class ConcreteReagent(models.Model):
    name = models.CharField(max_length=30)
    lot = models.CharField(max_length=30)
    concentration = models.ForeignKey(
        Concentration, related_name='reagent', on_delete=models.PROTECT)


class BufferMix(models.Model):
    concrete_reagents = models.ManyToManyField(ConcreteReagent)
    volume = models.PositiveIntegerField()
    final_volume = models.PositiveIntegerField()


class MixedReagent(models.Model):
    MIXED_REAGENT = 'mixed_reagent'
    buffer_mix = models.ForeignKey(BufferMix, 
        related_name=MIXED_REAGENT, on_delete=models.PROTECT)
    concentration = models.ForeignKey(Concentration, 
        related_name=MIXED_REAGENT, on_delete=models.PROTECT)


class PlaceholderReagent(models.Model):
    type = models.CharField(max_length=15, choices=PLACEHOLDER_CHOICES)
    concentration = models.ForeignKey(Concentration, 
        related_name='placeholder_reagent', on_delete=models.PROTECT)


class MasterMix(models.Model):
    water = models.ForeignKey(ConcreteReagent, 
        related_name='master_mix_water', on_delete=models.PROTECT)
    buffer_mix = models.ForeignKey(MixedReagent,
        related_name='master_mix_buffermix', on_delete=models.PROTECT)
    primers = models.ForeignKey(PlaceholderReagent,
        related_name='master_mix_primers', on_delete=models.PROTECT)
    hgDNA = models.ForeignKey(PlaceholderReagent,
        related_name='master_mix_hgDNA', null=True, on_delete=models.PROTECT)
    template = models.ForeignKey(PlaceholderReagent,
        related_name='master_mix_template', on_delete=models.PROTECT)
    final_volume = models.PositiveIntegerField()


class Gene(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Organism(models.Model):
    abbreviation = models.CharField(max_length=8, unique=True)
    full_name = models.CharField(max_length=30, unique=True)


class Primer(models.Model):
    oligo_code = models.CharField(max_length=30)
    full_name = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=15, choices=PRIMER_ROLE_CHOICES)
    organism = models.ForeignKey(Organism, 
        related_name='primer', on_delete=models.PROTECT)
    gene = models.ForeignKey(Gene, 
        related_name='primer', on_delete=models.PROTECT)


class PrimerPair(models.Model):
    forward_primer = models.ForeignKey(Primer, 
        related_name='primer_pair_fwd', on_delete=models.PROTECT)
    reverse_primer = models.ForeignKey(Primer, 
        related_name='primer_pair_rev', on_delete=models.PROTECT)
    suitable_for_pa = models.BooleanField()
    suitable_for_id = models.BooleanField()


class PrimerKit(models.Model):
    pa_primers = models.ManyToManyField(PrimerPair,
        related_name='primer_pair_pa')
    id_primers = models.ManyToManyField(PrimerPair,
        related_name='primer_pair_id')
    fwd_concentration = models.ForeignKey(Concentration, 
        related_name='primer_kit_fwd', on_delete=models.PROTECT)
    rev_concentration = models.ForeignKey(Concentration, 
        related_name='primer_kit_rev', on_delete=models.PROTECT)
    

class Arg(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Strain(models.Model):
    name = models.CharField(max_length=30, unique=True)
    organism = models.ForeignKey(Organism, 
        related_name='strain_organism', on_delete=models.PROTECT)
    arg = models.ForeignKey(Arg, 
        related_name='strain_arg', null=True, on_delete=models.PROTECT)
    genome_size = models.BigIntegerField()


class StrainKit(models.Model):
    strains = models.ManyToManyField(Strain)


class CyclingPattern(models.Model):
    activation_time = models.PositiveIntegerField()
    activation_temp = models.PositiveIntegerField()
    num_cycles = models.PositiveIntegerField()
    denature_temp = models.PositiveIntegerField()
    denature_time = models.PositiveIntegerField()
    anneal_temp = models.PositiveIntegerField()
    anneal_time = models.PositiveIntegerField()
    extend_temp = models.PositiveIntegerField()
    extend_time = models.PositiveIntegerField()


class Repeat(models.Model):
    """
    This is an allocation distribution pattern.

    Allocates the CSV strings it holds to consecutive columns, starting
    at its <start column>, and wrapping round to repeat itself. Stops when it
    reaches the <start column> cited by another Repeat object in the same group.
    Applies to its <start row> and all subsequent rows, until it reaches the
    start row of another Repeat object in the same group.
    """
    start_row = models.CharField(max_length=1)
    start_column = models.PositiveIntegerField()
    items_csv = models.CharField(max_length=200)

class Expansion(models.Model):
    """
    This is an allocation distribution pattern.

    Has-A column group width. E.g. 4.
    Allocates the first of its CSV strings to columns 1,2,3,4.
    Allocates the next of its CSV strings to columns 5,6,7,8.
    And so on.
    Applies to its <start row> and all subsequent rows, until it reaches the
    start row of another Expansion object in the same group.
    """
    column_group_width = models.PositiveIntegerField()
    start_row = models.CharField(max_length=1)
    items_csv = models.CharField(max_length=200)


class AllocationInstructions(models.Model):
    column_group_width = models.PositiveIntegerField() # e.g. 4

    # Strains repeat across column blocks, uniformly for all rows.
    strains = models.ForeignKey(Repeat, 
        related_name='allocation_strains', on_delete=models.PROTECT)

    # Strain copies requires a separate expansion for each column group, and 
    # also varies between rows.
    strain_copies = models.ManyToManyField(Expansion, 
        related_name='allocation_strains_copies')

    # Human dna requires a separate expansion for each column group, and also
    # varies between rows.
    gdna = models.ManyToManyField(Expansion,
        related_name='allocation_gdna')

    # PA primers require a separate dedicated list for each column group, but
    # is uniform for all rows. We use <Repeat> models, but their start columns
    # are configured so that they don't ever actually repeat.
    pa_primers = models.ManyToManyField(Repeat,
        related_name='allocation_primer_pa')

    # Dilution factor require a separate expansion for each column group, but
    # is uniform for all rows.
    dilution_factor = models.ManyToManyField(Expansion,
        related_name='allocation_dilution_factor')

    # ID Primers repeat across column blocks, uniformly for all rows.
    id_primers = models.ForeignKey(Repeat, 
        related_name='allocation_id_primers', on_delete=models.PROTECT)

    # e.g. "4, 8, 12"
    suppressed_columns = models.CharField(max_length=200) 


class Plate(models.Model):
    name = models.CharField(max_length=20) 
    allocation_instruction = models.ForeignKey(AllocationInstructions, 
        related_name='plate', on_delete=models.PROTECT)


class Experiment(models.Model):
    experiment_name = models.CharField(max_length=80, unique=True) 
    designer_name = models.CharField(max_length=80) 
    pa_mastermix = models.ForeignKey(MasterMix, 
        related_name='experiment_pa', on_delete=models.PROTECT)
    id_mastermix = models.ForeignKey(MasterMix, 
        related_name='experiment_id', on_delete=models.PROTECT)
    primer_kit = models.ForeignKey(PrimerKit, 
        related_name='experiment_primer_kit', on_delete=models.PROTECT)
    strain_kit = models.ForeignKey(StrainKit, 
        related_name='experiment_strain_kit', on_delete=models.PROTECT)
    plates = models.ManyToManyField(Plate)
    pa_cycling = models.ForeignKey(CyclingPattern, 
        related_name='experiment_pa_cycling', on_delete=models.PROTECT)
    id_cycling = models.ForeignKey(CyclingPattern, 
        related_name='experiment_id_cycling', on_delete=models.PROTECT)
