"""
Creates the minimum viable starter content for a virgin database.
For example primers, strains etc. Then a reference experiement..
"""

from app.models.reagent_models import *
from app.models.primer_models import *
from app.models.strain_models import *
from app.models.experiment_model import *
from app.models.plate_models import *


class ReferenceExperiment():
    """
    Creates all the database entities required to assemble an example,
    refrence models.Experiment, and returns the correpsonding instance.
    """

    def __init__(self):
        self.experiment = None
        self._next_count = 0 # To help generate incrementing numbers.

    def create(self):
        self._create_shared_entities() # Organisms, Stock reagents etc.
        self.experiment = self._create_experiment()
        return self.experiment

    #-----------------------------------------------------------------------
    # Private below.
    #-----------------------------------------------------------------------

    def _tick(self):
        self._next_count += 1
        return self._next_count

    def _create_shared_entities(self):
        self._create_reagents()
        self._create_organisms_and_strains()
        self._create_genes_and_primers()

    def _create_reagents(self):
        Reagent.make_from_quotient('BSA', '-', 20, 1, 'mg/ml')
        Reagent.make_from_quotient('DNA Free Water', '22884100', 1, 1, 'X')
        Reagent.make_from_quotient('dNTPs', '-', 10, 0.2, 'mM each')
        Reagent.make_from_quotient('KCl', '-', 1000, 48, 'mM')
        Reagent.make_from_quotient('KOH', '-', 100, 1, 'mM')
        Reagent.make_from_quotient('MgCl2', '449890', 25, 2.06, 'mM')
        Reagent.make_from_quotient(
            'Titanium PCR Buffer', '1602046A', 10, 0.13, 'X')
        Reagent.make_from_quotient('SYBRgreen', '-', 100, 0.32, 'X')
        Reagent.make_from_quotient('Titanium Taq', '1607230A', 50, 1.0, 'x')
        Reagent.make_from_quotient('Titanium Taq', '1607230A', 50, 1.3, 'x')
        Reagent.make_from_quotient('Triton', '-', 10, 0.04, '%')


    def _create_organisms_and_strains(self):
        self._create_organisms()
        self._create_args()
        self._create_strains()

    def _create_organisms(self):
        Organism.make('Eco', 'Escherichia coli')
        Organism.make('Efm', 'Enterococcus faecium')
        Organism.make('Efs', 'Enterococcus faecalis')
        Organism.make('Kox', 'Klebsiella oxytoca')
        Organism.make('Kpn', 'Klebsiella pneumoniae')
        Organism.make('Pmi', 'Proteus mirabilis')
        Organism.make('Spo', 'Schizosaccharomyces pombe')

    def _create_args(self):
        Arg.make('CTX-M9 TEM-WT')
        Arg.make('KPC')
        Arg.make('vanA')
        Arg.make('vanB')

    def _create_strains(self):

        Strain.make('ATCC 15764', 
            self._org('Kox'), None, 6684900)
        Strain.make('ATCC 26189', 
            self._org('Spo'), None, 12570000)
        Strain.make('ATCC 700802', 
            self._org('Efs'), self._arg('vanB'), 3220000)
        Strain.make('ATCC BAA-1705', 
            self._org('Kpn'), self._arg('KPC'), 5300000)
        Strain.make('ATCC BAA-2317', 
            self._org('Efm'), self._arg('vanA'), 2698130)
        Strain.make('ATCC BAA-2355', 
            self._org('Eco'), self._arg('vanA'), 4600000)
        Strain.make('ATCC BAA-633', 
            self._org('Pmi'), None, 4063000)

    def _org(self, abbr):
        return Organism.objects.get(abbreviation=abbr)

    def _arg(self, name):
        return Arg.objects.get(name=name)

    def _gene(self, name):
        return Gene.objects.get(name=name)

    def _prim(self, name):
        return Primer.objects.get(full_name=name)

        
    def _create_genes_and_primers(self):
        self._create_genes()
        self._create_primers()
        self._create_primer_pairs()

    def _create_genes(self):
        Gene.objects.create(name='cpn60')
        Gene.objects.create(name='gp')
        Gene.objects.create(name='khe')
        Gene.objects.create(name='peh')
        Gene.objects.create(name='uidA')
        Gene.objects.create(name='vanA')
        Gene.objects.create(name='zapA')
        Gene.objects.create(name='vanB')

    def _create_primers(self):
        # These are ordered and grouped first by organism.
        # Secondary groups by primer name.
        # Ordering with groups is PA then ID.
        # Secondary ordering is 'fwd' / 'rev'

        Primer.make(self._org('Eco'), 'Eco63', 'fwd', self._gene('uidA'))
        Primer.make(self._org('Eco'), 'Eco60', 'rev', self._gene('uidA'))
        Primer.make(self._org('Eco'), 'Eco64', 'fwd', self._gene('uidA'))
        Primer.make(self._org('Eco'), 'Eco66', 'rev', self._gene('uidA'))

        Primer.make(self._org('Efm'), 'van05', 'fwd', self._gene('vanA'))
        Primer.make(self._org('Efm'), 'van01', 'rev', self._gene('vanA'))
        Primer.make(self._org('Efm'), 'van04', 'fwd', self._gene('vanA'))
        Primer.make(self._org('Efm'), 'van02', 'rev', self._gene('vanA'))

        Primer.make(self._org('Efs'), 'Efs04', 'fwd', self._gene('cpn60'))
        Primer.make(self._org('Efs'), 'Efs01', 'rev', self._gene('cpn60'))
        Primer.make(self._org('Efs'), 'Efs03', 'fwd', self._gene('cpn60'))
        Primer.make(self._org('Efs'), 'Efs02', 'rev', self._gene('cpn60'))

        Primer.make(self._org('Efs'), 'van10', 'fwd', self._gene('vanB'))
        Primer.make(self._org('Efs'), 'van06', 'rev', self._gene('vanB'))
        Primer.make(self._org('Efs'), 'van30', 'fwd', self._gene('vanB'))
        Primer.make(self._org('Efs'), 'van33', 'rev', self._gene('vanB'))

        Primer.make(self._org('Kox'), 'Kox05', 'fwd', self._gene('peh'))
        Primer.make(self._org('Kox'), 'Kox02', 'rev', self._gene('peh'))
        Primer.make(self._org('Kox'), 'Kox04', 'fwd', self._gene('peh'))
        Primer.make(self._org('Kox'), 'Kox03', 'rev', self._gene('peh'))

        Primer.make(self._org('Kpn'), 'Kpn13', 'fwd', self._gene('khe'))
        Primer.make(self._org('Kpn'), 'Kpn01', 'rev', self._gene('khe'))
        Primer.make(self._org('Kpn'), 'Kpn03', 'fwd', self._gene('khe'))
        Primer.make(self._org('Kpn'), 'Kpn02', 'rev', self._gene('khe'))

        Primer.make(self._org('Pmi'), 'Pmi01', 'fwd', self._gene('zapA'))
        Primer.make(self._org('Pmi'), 'Pmi05', 'rev', self._gene('zapA'))
        Primer.make(self._org('Pmi'), 'Pmi02', 'fwd', self._gene('zapA'))
        Primer.make(self._org('Pmi'), 'Pmi03', 'rev', self._gene('zapA'))

        Primer.make(self._org('Spo'), 'Spo09', 'fwd', self._gene('gp'))
        Primer.make(self._org('Spo'), 'Spo13', 'rev', self._gene('gp'))
        Primer.make(self._org('Spo'), 'Spo03', 'fwd', self._gene('gp'))
        Primer.make(self._org('Spo'), 'Spo05', 'rev', self._gene('gp'))

    def _create_primer_pairs(self):
        PrimerPair.make(self._prim('Eco63'), self._prim('Eco60'), True, False)
        PrimerPair.make(self._prim('Efs04'), self._prim('Efs01'), True, False)
        PrimerPair.make(self._prim('van10'), self._prim('van06'), True, False)
        PrimerPair.make(self._prim('van05'), self._prim('van01'), True, False)
        PrimerPair.make(self._prim('Kox05'), self._prim('Kox02'), True, False)
        PrimerPair.make(self._prim('Kpn13'), self._prim('Kpn01'), True, False)
        PrimerPair.make(self._prim('Pmi01'), self._prim('Pmi05'), True, False)
        PrimerPair.make(self._prim('Spo09'), self._prim('Spo13'), True, False)

        PrimerPair.make(self._prim('Eco64'), self._prim('Eco66'), False, True)
        PrimerPair.make(self._prim('Efs03'), self._prim('Efs02'), False, True)
        PrimerPair.make(self._prim('van30'), self._prim('van33'), False, True)
        PrimerPair.make(self._prim('van04'), self._prim('van02'), False, True)
        PrimerPair.make(self._prim('Kox04'), self._prim('Kox03'), False, True)
        PrimerPair.make(self._prim('Kpn03'), self._prim('Kpn02'), False, True)
        PrimerPair.make(self._prim('Pmi02'), self._prim('Pmi03'), False, True)
        PrimerPair.make(self._prim('Spo03'), self._prim('Spo05'), False, True)


    def _create_experiment(self):
        return Experiment.make(
            'reference_experiment_1',
            'PH',
            [self._create_plate_1('plate_1')], 
            self._create_pa_cycling(),
            self._create_id_cycling(),
        )


    def _make_pa_primers(self):
        res = []
        res.append(self._find_pa_primer_pair('Eco63', 'Eco60'))
        res.append(self._find_pa_primer_pair('Efs04', 'Efs01'))
        res.append(self._find_pa_primer_pair('van10', 'van06'))
        res.append(self._find_pa_primer_pair('van05', 'van01'))
        res.append(self._find_pa_primer_pair('Kox05', 'Kox02'))
        res.append(self._find_pa_primer_pair('Kpn13', 'Kpn01'))
        res.append(self._find_pa_primer_pair('Pmi01', 'Pmi05'))
        res.append(self._find_pa_primer_pair('Spo09', 'Spo13'))
        return res

    def _make_id_primers(self):
        res = []
        res.append(self._find_id_primer_pair('Eco64', 'Eco66'))
        res.append(self._find_id_primer_pair('Efs03', 'Efs02'))
        res.append(self._find_id_primer_pair('van30', 'van33'))
        res.append(self._find_id_primer_pair('van04', 'van02'))
        res.append(self._find_id_primer_pair('Kox04', 'Kox03'))
        res.append(self._find_id_primer_pair('Kpn03', 'Kpn02'))
        res.append(self._find_id_primer_pair('Pmi02', 'Pmi03'))
        res.append(self._find_id_primer_pair('Spo03', 'Spo05'))
        return res

    def _find_id_primer_pair(self, fwd_name, rev_name):
        primer_pair = PrimerPair.objects.get(
            forward_primer__full_name=fwd_name,
            reverse_primer__full_name=rev_name,
            suitable_for_id=True,
            )
        return primer_pair

    def _find_pa_primer_pair(self, fwd_name, rev_name):
        primer_pair = PrimerPair.objects.get(
            forward_primer__full_name=fwd_name,
            reverse_primer__full_name=rev_name,
            suitable_for_pa=True,
            )
        return primer_pair

    def _find_primer_pair(self, fwd_name, rev_name, 
            suitable_for_pa, suitable_for_id):
        primer_pair = PrimerPair.objects.get(
            forward_primer__full_name=fwd_name,
            reverse_primer__full_name=rev_name,
            suitable_for_pa=suitable_for_pa,
            suitable_for_id=suitable_for_id,
            )
        return primer_pair



    def _create_pa_cycling(self):
        return CyclingPattern.make(
            activation_time=120,
            activation_temp=95,
            num_cycles=20,
            denature_time=10,
            denature_temp=95,
            anneal_time=10,
            anneal_temp=62,
            extend_temp=72,
            extend_time=30
        )

    def _create_id_cycling(self):
        return CyclingPattern.make(
            activation_time=120,
            activation_temp=95,
            num_cycles=20,
            denature_time=10,
            denature_temp=95,
            anneal_time=0,
            anneal_temp=0,
            extend_temp=62,
            extend_time=25
        )

    def _create_plate_1(self, experiment_name):
        return Plate.make(
            experiment_name + '_1',
            self._make_allocation_1()
        )

    def _make_allocation_1(self):

        return AllocationInstructions.make(
            RuleList.make(self._rule_list()),
            '4, 8, 12'
        )

    def _rule_list(self):
        rules = []
        rules.extend(self._strains_rules_1())
        rules.extend(self._strains_copies_rules_1())
        rules.extend(self._hg_dna_rules_1())
        rules.extend(self._pa_primers_rules_1())
        rules.extend(self._dilution_factor_rules_1())
        rules.extend(self._id_primers_rules_1())

        return rules


    def _strains_rules_1(self):
        # Same pattern repeated every 4 columns, same for all rows.
        data = (
            ('ATCC BAA-2355',('A', 'H', 1, 4)),
            ('ATCC 700802',('A', 'H', 4, 8)),
            ('ATCC 15764',('A', 'H', 8, 12),)
        )
        return self._rules_from_data('Strain', data)

    def _strains_copies_rules_1(self):
        # Blanket fill with 5's everwhere first
        # Then, first two rows - filled with zeros.
        # Then, larger numbers in small zones.
        data = (
            ('5', ('A', 'H', 1, 12)),
            ('0', ('A', 'B', 1, 12)),
            ('50', ('C', 'D', 9, 12)),
            ('500', ('E', 'F', 9, 12)),
            ('5000', ('G', 'H', 9, 12)),
        )
        return self._rules_from_data('Strain Count', data)


    def _hg_dna_rules_1(self):
        # Distribution in English.
        # Blanket fill with 0 everywhere.
        # Then 3000 in a bottom left block.
        data = (
            ('0', ('A', 'H', 1, 12)),
            ('5000', ('F', 'H', 1, 8)),
        )
        return self._rules_from_data('HgDNA', data)

    def _pa_primers_rules_1(self):
        # Distribution in English.
        # Columns split into 3 groups, each with its own block allocation.
        # Uniform for all rows.

        data = (
            ('poolB1',('A', 'H', 1, 4)),
            ('Eco63 Eco60',  ('A', 'H', 5, 5)),
            ('Efs04 Efs01', ('A', 'H', 6, 6)),
            ('van10 van06', ('A', 'H', 7, 7)),
            ('van05 van01', ('A', 'H', 8, 8)),
            ('', ('A', 'H', 9, 12)),
        )
        return self._rules_from_data('PA Primers', data)


    def _dilution_factor_rules_1(self):
        # Distribution in English.
        # One constant value for left two thirds, and another for
        # remaining two thirds.
        data = (
            ('30', ('A', 'H', 1, 8)),
            ('', ('A', 'H', 9, 12)),
        )
        return self._rules_from_data('Dilution Factor', data)

    def _id_primers_rules_1(self):
        # Distribution in English.
        # One block repeating every 4 columns, for all rows.
        primer_block = 'Eco64 Eco66, Efs03 Efs02, van30 van33, van04 van02'
        data = (
            ('Eco64 Eco66', ('A', 'H', 1, 3)),
            ('Efs03 Efs02', ('A', 'H', 3, 6)),
            ('van30 van33', ('A', 'H', 6, 9)),
            ('van04 van02', ('A', 'H', 9, 12)),
        )
        return self._rules_from_data('ID-Primers', data)

    def _rules_from_data(self, payload_type, data):
        rules = []
        for rule in data:
            payload, zone = rule
            rules.append(AllocRule.make(self._tick(), 
                payload_type, payload, zone))
        return rules

if __name__ == "__main__":
    ReferenceExperiment().create()

