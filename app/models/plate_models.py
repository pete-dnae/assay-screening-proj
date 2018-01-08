from django.db import models

from .odds_and_ends_models import mk_choices

class AllocRule(models.Model):

    payload_choices = mk_choices((
        'Strain',
        'Strain Count',
        'HgDNA',
        'PA Primers',
        'Dilution Factor',
        'ID Primers'))

    pattern_choices = mk_choices(('Consecutive', 'In Blocks'))

    rank_for_ordering = models.DecimalField(max_digits=8, decimal_places=2)
    payload_type = models.CharField(max_length=15, choices=payload_choices)
    payload_csv = models.CharField(max_length=500)
    pattern = models.CharField(max_length=15, choices=pattern_choices)
    start_row_letter = models.CharField(max_length=1)
    end_row_letter = models.CharField(max_length=1)
    start_column = models.PositiveIntegerField()
    end_column = models.PositiveIntegerField()

    class Meta:
        ordering = ('rank_for_ordering',)

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
            self.payload_type,
            payload,
            self.pattern,
            'Rows:%s-%s, Cols:%d-%d' % (
                self.start_row_letter,
                self.end_row_letter,
                self.start_column,
                self.end_column
            ),
        ))



class AllocationInstructions(models.Model):
    allocation_rules = models.ManyToManyField(AllocRule)
    suppressed_columns = models.CharField(max_length=200) 


class Plate(models.Model):
    name = models.CharField(max_length=20) 
    allocation_instructions = models.ForeignKey(AllocationInstructions, 
        related_name='plate', on_delete=models.PROTECT)
