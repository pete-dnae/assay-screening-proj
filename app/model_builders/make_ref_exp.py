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
        self._create_concentrations()
        self._create_organisms_and_strains()
        self._create_buffer_reagents()
        self._create_hgdna_reagents()
        self._create_genes_and_primers()

    def _create_concentrations(self):
        for denom, numerator, pref_units in (
                (1, 1, 'X'),
                (10, 0.13, 'X'),
                (10, 0.2, 'mM'),
                (10, 0.04, '%'),
                (20, 1, 'mg/ml'),
                (25, 2.06, 'mM'),
                (50, 1.0, 'x'),
                (50, 1.3, 'x'),
                (100, 0.32, 'X'),
                (100, 1, 'mM'),
                (1000, 48, 'mM')):
            Concentration.make(numerator / float(denom), pref_units)


    def _create_buffer_reagents(self):
        Reagent.make('BSA', '-', self._conc_rat(20, 1, 'mg/ml'))
        Reagent.make('DNA Free Water', '22884100', self._conc_rat(1, 1, 'X'))
        Reagent.make('dNTPs', '-', self._conc_rat(10, 0.2, 'mM'))
        Reagent.make('KCl', '-', self._conc_rat(1000, 48, 'mM'))
        Reagent.make('KOH', '-', self._conc_rat(100, 1, 'mM'))
        Reagent.make('MgCl2', '449890', self._conc_rat(25, 2.06, 'mM'))
        Reagent.make('Titanium PCR Buffer', '1602046A', 
            self._conc_rat(10, 0.13, 'X'))
        Reagent.make('SYBRgreen', '-', self._conc_rat(100, 0.32, 'X'))
        Reagent.make('Titanium Taq', '1607230A', self._conc_rat(50, 1.0, 'x'))
        Reagent.make('Titanium Taq', '1607230A', self._conc_rat(50, 1.3, 'x'))
        Reagent.make('Triton', '-', self._conc_rat(10, 0.04, '%'))



    def _create_hgdna_reagents(self):
        for count in (0, 5000):
            # TODO this is not the correct concentration value.
            conc = Concentration.make(count, 'X')
            Reagent.make('hgDNA', '-', conc)


    def _create_organisms_and_strains(self):
        self._create_organisms()
        self._create_args()
        self._create_strain_reagents()

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

    def _create_strain_reagents(self):
        for strain_name, org_name, arg_name, genome_len in (
                ('ATCC 15764', 'Kox', None, 6684900),
                ('ATCC 26189', 'Spo', None, 12570000),
                ('ATCC 700802', 'Efs', 'vanB', 3220000),
                ('ATCC BAA-1705', 'Kpn', 'KPC', 5300000),
                ('ATCC BAA-2317', 'Efm', 'vanA', 2698130),
                ('ATCC BAA-2355', 'Eco', 'vanA', 4600000),
                ('ATCC BAA-633', 'Pmi', None, 4063000)):
            arg = None if arg_name is None else self._arg(arg_name)
            Strain.make(strain_name, self._org(org_name), arg, genome_len)
            for count in (5, 50, 500, 5000):
                # TODO this is not the correct conversion between a strain count
                # and a concentration value.
                conc = Concentration.make(count, 'X')
                Reagent.make(strain_name, '-', conc)
        
    def _create_genes_and_primers(self):
        self._create_genes()
        self._create_primer_reagents()
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

    def _create_primer_reagents(self):
        # These are ordered and grouped first by organism.
        # Secondary groups by primer name.
        # Ordering with groups is PA then ID.
        # Secondary ordering is 'fwd' / 'rev'

        for organism_name,primer_name,role,gene_name in(('Eco','Eco63','fwd','uidA'),('Eco','Eco60','rev','uidA'),
                                                        ('Eco','Eco64','fwd','uidA'),('Eco','Eco66','rev','uidA'),
                                                        ('Efm', 'van05', 'fwd', 'vanA'),('Efm', 'van01', 'rev', 'vanA'),
                                                        ('Efm', 'van04', 'fwd', 'vanA'),('Efm', 'van02', 'rev', 'vanA'),
                                                        ('Efs', 'Efs04', 'fwd', 'cpn60'),('Efs', 'Efs01', 'rev', 'cpn60'),
                                                        ('Efs', 'Efs03', 'fwd', 'cpn60'),('Efs', 'Efs02', 'rev', 'cpn60'),
                                                        ('Efs', 'van10', 'fwd', 'vanB'),('Efs', 'van06', 'rev', 'vanB'),
                                                        ('Efs', 'van30', 'fwd', 'vanB'),('Efs', 'van33', 'rev', 'vanB'),
                                                        ('Kox', 'Kox05', 'fwd', 'peh'),('Kox', 'Kox02', 'rev', 'peh'),
                                                        ('Kox', 'Kox04', 'fwd', 'peh'),('Kox', 'Kox03', 'rev', 'peh'),
                                                        ('Kpn', 'Kpn13', 'fwd', 'khe'),('Kpn', 'Kpn01', 'rev', 'khe'),
                                                        ('Kpn', 'Kpn03', 'fwd', 'khe'),('Kpn', 'Kpn02', 'rev', 'khe'),
                                                        ('Pmi', 'Pmi01', 'fwd', 'zapA'),('Pmi', 'Pmi05', 'rev', 'zapA'),
                                                        ('Pmi', 'Pmi02', 'fwd', 'zapA'),('Pmi', 'Pmi03', 'rev', 'zapA'),
                                                        ('Spo', 'Spo09', 'fwd', 'gp'),('Spo', 'Spo13', 'rev', 'gp'),
                                                        ('Spo', 'Spo03', 'fwd', 'gp'),('Spo', 'Spo05', 'rev', 'gp')):

            Primer.make(self._org(organism_name), primer_name,role, self._gene(gene_name))
            conc = Concentration.make(0.4, 'microM')
            Reagent.make(primer_name, '-', conc)

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
        rules.extend(self._hg_dna_rules_1())
        rules.extend(self._pa_primers_rules_1())
        rules.extend(self._id_primers_rules_1())
        return rules


    def _strains_rules_1(self):
        data = (
            (self._reagent(Reagent.make_hash('ATCC BAA-2355',Concentration.value_from_quotient(1, 5000))),('A', 'H', 1, 4)),
            (self._reagent(Reagent.make_hash('ATCC 700802',Concentration.value_from_quotient(1, 50))),('A', 'H', 4, 8)),
            (self._reagent(Reagent.make_hash('ATCC 15764',Concentration.value_from_quotient(1, 500))),('A', 'H', 8, 12),)
        )
        return self._rules_from_data('Strain', data)

    def _hg_dna_rules_1(self):
        # Distribution in English.
        # Blanket fill with 0 everywhere.
        # Then 3000 in a bottom left block.
        data = (
            (self._reagent(Reagent.make_hash('hgDNA',Concentration.value_from_quotient(1, 0))), ('A', 'H', 1, 12)),
            (self._reagent(Reagent.make_hash('hgDNA',Concentration.value_from_quotient(1, 5000))), ('F', 'H', 1, 8)),
        )
        return self._rules_from_data('HgDNA', data)

    def _pa_primers_rules_1(self):
        # Distribution in English.
        # Columns split into 3 groups, each with its own block allocation.
        # Uniform for all rows.

        data = (
            (self._reagent(Reagent.make_hash('Eco63',Concentration.value_from_quotient(1, 0.4))),  ('A', 'H', 5, 5)),
            (self._reagent(Reagent.make_hash('Eco60', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 5, 5)),
            (self._reagent(Reagent.make_hash('Efs04', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 6, 6)),
            (self._reagent(Reagent.make_hash('Efs01', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 6, 6)),
            (self._reagent(Reagent.make_hash('van10', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 7, 7)),
            (self._reagent(Reagent.make_hash('van06', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 7, 7)),
            (self._reagent(Reagent.make_hash('van05', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 8, 8)),
            (self._reagent(Reagent.make_hash('van01',Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 8, 8)),
            (self._reagent(Reagent.make_hash('Spo09', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 8, 8)),
            (self._reagent(Reagent.make_hash('Spo13', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 8, 8)),

        )
        return self._rules_from_data('PA Primers', data)

    def _id_primers_rules_1(self):
        # Distribution in English.
        # One block repeating every 4 columns, for all rows.
        primer_block = 'Eco64 Eco66, Efs03 Efs02, van30 van33, van04 van02'
        data = (
            (self._reagent(Reagent.make_hash('Eco64', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 1, 3)),
            (self._reagent(Reagent.make_hash('Eco66', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 1, 3)),
            (self._reagent(Reagent.make_hash('Efs03', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 3, 6)),
            (self._reagent(Reagent.make_hash('Efs02', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 3, 6)),
            (self._reagent(Reagent.make_hash('van30', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 6, 9)),
            (self._reagent(Reagent.make_hash('van33', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 6, 9)),
            (self._reagent(Reagent.make_hash('van04', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 9, 12)),
            (self._reagent(Reagent.make_hash('van01', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 9, 12)),
        )
        return self._rules_from_data('ID-Primers', data)

    def _rules_from_data(self, payload_type, data):
        rules = []
        for rule in data:
            payload, zone = rule
            rules.append(AllocRule.make(self._tick(), 
                payload_type, payload, zone))
        return rules

    """
    A few 'finder' methods.
    """


    def _conc_rat(self, denom, numerator, pref_units):
        # Find a Concentration from a rational number (fraction)
        string_value = Concentration.value_from_quotient(denom, numerator)
        return Concentration.objects.get(
            normalised_string_value=string_value, preferred_units=pref_units)


    def _conc_str(self, normalised_string_value, pref_units):
        # Find a Concentration from its normalised string value.
        return Concentration.objects.get(
            normalised_string_value=normalised_string_value,
            preferred_units=pref_units)


    def _org(self, abbr):
        return Organism.objects.get(abbreviation=abbr)


    def _arg(self, name):
        return Arg.objects.get(name=name)


    def _gene(self, name):
        return Gene.objects.get(name=name)


    def _prim(self, name):
        return Primer.objects.get(full_name=name)


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

    def _reagent(self, reagent_hash):
        """
        Example reagent_hash could be: 'ATCC 26189:5.000e+01'
        """
        return Reagent.objects.get(hash=reagent_hash)

if __name__ == "__main__":
    ReferenceExperiment().create()

