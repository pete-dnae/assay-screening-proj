from django.db import models

from .odds_and_ends_models import mk_choices

class Allocatable(models.Model):
    """ 
    A place to define which things are "allocatable" to cells on a plate.
    For example Pre-Amp Primer, or Strain etc. The wider system
    is built with the aspiration that this set of types can be grown and
    altered simply by adding things to this table at runtime rather than
    changing the code and requiring a new build and deployment.
    """
    type = models.CharField(primary_key=True, max_length=20)

    class Meta:
        ordering = ('type',) # Handy to have alphabetical order.


class AllocRule(models.Model):

    pattern_choices = mk_choices(('Consecutive', 'In Blocks'))

    rank_for_ordering = models.PositiveIntegerField()
    payload_type = models.ForeignKey(Allocatable, 
        related_name='alloc_rule', on_delete=models.PROTECT)
    payload_csv = models.CharField(max_length=500)
    pattern = models.CharField(max_length=15, choices=pattern_choices)
    start_row_letter = models.CharField(max_length=1)
    end_row_letter = models.CharField(max_length=1)
    start_column = models.PositiveIntegerField() # Start at 1, not zero
    end_column = models.PositiveIntegerField() # Start at 1, not zero

    class Meta:
        ordering = ('rank_for_ordering',)

    def enumerate_applicable_rows(self):
        start = ord(self.start_row_letter) - ord('A')
        end = ord(self.end_row_letter) - ord('A')
        return [i for i in range(start, end + 1)]

    def number_of_columns(self):
        return 1 + self.end_column - self.start_column

    def enumerate_column_indices(self):
        return [i for i in range(self.start_column - 1, self.end_column)]

    def payload_items(self):
        items = self.payload_csv.split(',')
        items = [i.strip() for i in items]
        return items

    def display_string(self):
        """
        E.g.
        'Strain Count, (ATCC BAA-2355, AT...), In Blocks, Rows:A-H, Cols:1-12'
        """
        payload = self.payload_csv
        LIMIT = 17
        if len(self.payload_csv) > LIMIT:
            payload = self.payload_csv[:LIMIT] + '...'
        return('%s, (%s), %s, %s' % (
            self.payload_type.type,
            payload,
            self.pattern,
            'Rows:%s-%s, Cols:%d-%d' % (
                self.start_row_letter,
                self.end_row_letter,
                self.start_column,
                self.end_column

            ),
        ))

    
    @classmethod
    def make_placeholder_rule(cls):
        rule = AllocRule.objects.create(
            rank_for_ordering = 0,
            # Note the next line won't execute unless the db is populated!
            payload_type = Allocatable.objects.get(type='Unspecified'),
            payload_csv = '',
            pattern = 'Consecutive',
            start_row_letter = 'A',
            end_row_letter = 'B',
            start_column = 1,
            end_column = 2,
        )
        rule.save()
        return rule


class RuleList(models.Model):
    """
    A class that encapsulates a list of AllocRule(s) by wrapping a 
    ManyToManyField of them, and by providing a few convenience methods on 
    the list.
    """
    rules = models.ManyToManyField(AllocRule)

    @classmethod
    def apply_ranking_order_to_rule_objs(cls, rules):
        """
        Changes the *rank_for_ordering* field on the supplied list of
        AllocRule(s) to match the order in which they appear in the list.
        """
        for count, rule in enumerate(list(rules)):
            rule.rank_for_ordering = count
            rule.save()

    @classmethod
    def apply_ranking_order_to_rule_ids(cls, rule_ids):
        """
        A wrapper around the sister method above that takes a list of
        id(s) instead of a list of instances.
        """
        # We want to iterate over the rule_ids in the given order, so avoid
        # the mistake of accessing the AllocRule objects using a filter -
        # becasue that will defeat the order mandated by the list, and re-sort
        # according to the model's intrinsic ordering behaviour.
        rules = [AllocRule.objects.get(pk=rule_id) for rule_id in rule_ids]
        cls.apply_ranking_order_to_rule_objs(rules)

    @classmethod
    def make_copy_of(cls, rule_id_to_copy):
        """
        Makes a copy the specified AllocRule and saves it as a new, 
        independent instance.
        """
        # Allow DoesNotExist exception to propagate when so.
        rule = AllocRule.objects.get(pk=rule_id_to_copy)
        rule.pk = None
        rule.id = None
        rule.save()
        return rule


class AllocationInstructions(models.Model):
    rule_list = models.ForeignKey(RuleList, 
        related_name='instructions', on_delete=models.PROTECT)
    suppressed_columns = models.CharField(max_length=200) 


class Plate(models.Model):
    name = models.CharField(max_length=20) 
    allocation_instructions = models.ForeignKey(AllocationInstructions, 
        related_name='plate', on_delete=models.PROTECT)
