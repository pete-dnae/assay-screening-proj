"""
A group of closely related model classes, which taken together define the
reagent allocations for a Plate.
"""


import re

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxValueValidator

from .odds_and_ends_models import mk_choices
from .reagent_models import Reagent


class AllocRule(models.Model):
    """
    *Alloc Rule* is short for "Allocation Rule".

    It encapsulates a recipe for repeating patterns of things like *primers,
    strains, HgDNA* (and similar) to a rectangular region of an imaginary table.
    The type of thing being repeated is specified in the *payload_type* field,
    and must be one of the following:
        
        Dilution Factor
        HgDNA
        PA Primers
        ID Primers
        Strain
        Strain Count

    
    The target region of the table is defined in terms of row and column
    ranges.
    """

    payload_choices = mk_choices((
        'Dilution Factor',
        'HgDNA',
        'PA Primers',
        'ID Primers',
        'Strain',
        'Strain Count',
        'Reagent'))


    # This field is used to force some collections of AllocRule(s) to maintain
    # a strict sequence with respect to others in the same collection. It gets
    # updated later, only when AllocRule instances get put into RuleList
    # containers.
    rank_for_ordering = models.PositiveIntegerField(default=1)
    payload_type = models.CharField(max_length=15, choices=payload_choices)
    payload = models.ForeignKey(Reagent, 
        related_name='allocrule', on_delete=models.PROTECT)
    letter = RegexValidator(re.compile(r'[A-Z]'), 'Enter a capital letter.')
    start_row_letter = models.CharField(max_length=1, validators=[letter,])
    end_row_letter = models.CharField(max_length=1, validators=[letter,])

    max_column = MaxValueValidator(20)
    # First column is 1, not zero.
    start_column = models.PositiveSmallIntegerField(validators=[max_column,])
    end_column = models.PositiveSmallIntegerField(validators=[max_column,])

    # See also, whole-model validation checks in self.clean()

    class Meta:
        ordering = ('rank_for_ordering',)

    def save(self, *args, **kwargs):
        """
        We override model.save() in order to perform some
        whole-model consistency checks (like start column is not less than end
        column).
        """
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        """
        Ensure the start and end values for the row and column ranges
        do not contradict each other.
        """
        if self.start_row_letter > self.end_row_letter:
            raise ValidationError(
                'Start row must not be greater than end row')
        if self.start_column > self.end_column:
            raise ValidationError(
                'Start column must not be greater than end column')

    @classmethod
    def make(cls, rank_for_ordering, payload_type, payload, zone):
        sr, er, sc, ec = zone
        return AllocRule.objects.create(
            rank_for_ordering=rank_for_ordering,
            payload_type=payload_type,
            payload=payload,
            start_row_letter=sr,
            end_row_letter=er,
            start_column=sc,
            end_column=ec,
        )

    @classmethod
    def clone(cls, src):
        return cls.make(
            src.rank_for_ordering, # Plain copy
            src.payload_type, # Plain copy
            src.payload, # Shared reuse
            ( # Plain copy
                src.start_row_letter, 
                src.end_row_letter,
                src.start_column,
                src.end_column
            )
        )

    def enumerate_applicable_rows(self):
        start = ord(self.start_row_letter) - ord('A')
        end = ord(self.end_row_letter) - ord('A')
        return [i for i in range(start, end + 1)]

    def number_of_columns(self):
        return 1 + self.end_column - self.start_column

    def enumerate_column_indices(self):
        return [i for i in range(self.start_column - 1, self.end_column)]

    # todo consider moving this into __str or __repr
    def display_string(self):
        """
        E.g.
        'Strain, ATCC BAA-2355, Rows:A-H, Cols:1-12'
        """
        return('%s, %s,%s' % (
            self.payload_type,
            payload.name,
            'Rows:%s-%s, Cols:%d-%d' % (
                self.start_row_letter,
                self.end_row_letter,
                self.start_column,
                self.end_column

            ),
        ))

    
class RuleList(models.Model):
    """
    Encapsulates a list of AllocRule(s) by wrapping a 
    ManyToManyField of them, and managing each rule's *rank_for_ordering*
    field, in order to force them into a deliberate sequence.
    """
    rules = models.ManyToManyField(AllocRule)

    @classmethod
    def apply_ranking_order_to_rule_objs(cls, rules):
        """
        Changes the *rank_for_ordering* field on the supplied list of
        AllocRule(s) to match the order in which they appear in that list.
        """
        for count, rule in enumerate(list(rules)):
            rule.rank_for_ordering = count
            rule.save()

    @classmethod
    def make(cls, rules):
        rule_list = RuleList.objects.create(
        )
        for rule in rules:
            rule_list.rules.add(rule)
        rule_list.save()
        return rule_list

    @classmethod
    def clone(cls, src):
        return cls.make(
            [AllocRule.clone(rule) for rule in src.rules.all()] # New
        )


class AllocationInstructions(models.Model):
    """
    A container for a RuleList, plus meta data for that rule list. Meta data
    anticipated so far, is to say that some of the chamber allocations created
    by applying the rules, are to be ignored because some entire columns were
    found to be inviable in the lab during an experiment.
    """
    rule_list = models.ForeignKey(RuleList, 
        related_name='instructions', on_delete=models.PROTECT)
    suppressed_columns = models.CharField(max_length=200) 

    @classmethod
    def make(cls, rule_list, suppressed_columns):
        return AllocationInstructions.objects.create(
            rule_list=rule_list,
            suppressed_columns = suppressed_columns
        )

    @classmethod
    def clone(cls, src):
        return cls.make(
            RuleList.clone(src.rule_list), # New
            src.suppressed_columns # Plain copy
        )


class Plate(models.Model):
    """
    Represents a rectangular grid of chambers or wells (of indefinite size),
    that can have reagents put in them. It has a name so that people can
    identify several plates in an experiment, and it owns an
    AllocationInstruction object that defines the reagents allocated to each of
    its chambers.
    """
    name = models.CharField(max_length=20) 
    allocation_instructions = models.ForeignKey(AllocationInstructions, 
        related_name='plate', on_delete=models.PROTECT)

    @classmethod
    def make(cls, name, allocation_instructions):
        return Plate.objects.create(
            name=name,
            allocation_instructions=allocation_instructions
        )

    @classmethod
    def clone(cls, src):
        return cls.make(
            src.name + '_1', # Increment name
            AllocationInstructions.clone(src.allocation_instructions) # New
        )
