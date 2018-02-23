"""
Creates the minimum viable starter content for a virgin database.
For example primers, strains etc. Then a reference experiement..
"""

from app.models.reagent_models import *
from app.models.primer_models import *
from app.models.strain_models import *
from app.models.experiment_model import *
from app.models.rule_models import *
from .finders import Finders
from app.model_builders.common_modules import CreateExperiment

class ReferenceExperiment():
    """
    Creates all the database entities required to assemble an example,
    refrence models.Experiment, and returns the correpsonding instance.
    """

    def __init__(self):
        self.experiment = None

    def create(self):
        self._create_shared_entities() # Organisms, Stock reagents etc.
        self.experiment = self._create_experiment()
        return self.experiment

    #-----------------------------------------------------------------------
    # Private below.
    #-----------------------------------------------------------------------

    def _create_shared_entities(self):
        exp=CreateExperiment()
        exp._create_concentrations()
        self._create_organisms_and_strains()
        self._create_buffer_reagents()
        self._create_hgdna_reagents()
        self._create_genes_and_primers()

    def _create_buffer_reagents(self):
        finder=Finders()
        Reagent.make('BSA', '-', finder._conc_rat(20, 1, 'mg/ml'))
        Reagent.make('DNA Free Water', '22884100', finder._conc_rat(1, 1, 'X'))
        Reagent.make('dNTPs', '-', finder._conc_rat(10, 0.2, 'mM'))
        Reagent.make('KCl', '-', finder._conc_rat(1000, 48, 'mM'))
        Reagent.make('KOH', '-', finder._conc_rat(100, 1, 'mM'))
        Reagent.make('MgCl2', '449890', finder._conc_rat(25, 2.06, 'mM'))
        Reagent.make('Titanium PCR Buffer', '1602046A',
                     finder._conc_rat(10, 0.13, 'X'))
        Reagent.make('SYBRgreen', '-', finder._conc_rat(100, 0.32, 'X'))
        Reagent.make('Titanium Taq', '1607230A', finder._conc_rat(50, 1.0, 'x'))
        Reagent.make('Titanium Taq', '1607230A', finder._conc_rat(50, 1.3, 'x'))
        Reagent.make('Triton', '-', finder._conc_rat(10, 0.04, '%'))



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
        finder = Finders()
        for strain_name, org_name, arg_name, genome_len in (
                ('ATCC 15764', 'Kox', None, 6684900),
                ('ATCC 26189', 'Spo', None, 12570000),
                ('ATCC 700802', 'Efs', 'vanB', 3220000),
                ('ATCC BAA-1705', 'Kpn', 'KPC', 5300000),
                ('ATCC BAA-2317', 'Efm', 'vanA', 2698130),
                ('ATCC BAA-2355', 'Eco', 'vanA', 4600000),
                ('ATCC BAA-633', 'Pmi', None, 4063000)):
            arg = None if arg_name is None else finder._arg(arg_name)
            Strain.make(strain_name, finder._org(org_name), arg, genome_len)
            for count in (5, 50, 500, 5000):
                # TODO this is not the correct conversion between a strain count
                # and a concentration value.
                conc = Concentration.make(count, 'X')
                Reagent.make(strain_name, '-', conc)
        
    def _create_genes_and_primers(self):
        self._create_genes()
        self._create_primer_reagents()

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
        finder = Finders()
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

            Primer.make(finder._org(organism_name), primer_name,role, finder._gene(gene_name))
            conc = Concentration.make(0.4, 'microM')
            Reagent.make(primer_name, '-', conc)

    def _create_experiment(self):
        experiment = CreateExperiment()
        return Experiment.make(
            'reference_experiment_1',
            'PH',
            [self._create_plate_1('plate_1')],
            experiment._create_pa_cycling(),
            experiment._create_id_cycling(),
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
        finder = Finders()
        experiment = CreateExperiment()
        data = (
            (finder._reagent(Reagent.make_hash('ATCC BAA-2355',Concentration.value_from_quotient(1, 5000))),('A', 'H', 1, 4)),
            (finder._reagent(Reagent.make_hash('ATCC 700802',Concentration.value_from_quotient(1, 50))),('A', 'H', 4, 8)),
            (finder._reagent(Reagent.make_hash('ATCC 15764',Concentration.value_from_quotient(1, 500))),('A', 'H', 8, 12),)
        )
        return experiment._rules_from_data('Strain', data)

    def _hg_dna_rules_1(self):
        # Distribution in English.
        # Blanket fill with 0 everywhere.
        # Then 3000 in a bottom left block.
        finder = Finders()
        experiment = CreateExperiment()
        data = (
            (finder._reagent(Reagent.make_hash('hgDNA',Concentration.value_from_quotient(1, 0))), ('A', 'H', 1, 12)),
            (finder._reagent(Reagent.make_hash('hgDNA',Concentration.value_from_quotient(1, 5000))), ('F', 'H', 1, 8)),
        )
        return experiment._rules_from_data('HgDNA', data)

    def _pa_primers_rules_1(self):
        # Distribution in English.
        # Columns split into 3 groups, each with its own block allocation.
        # Uniform for all rows.
        finder = Finders()
        experiment = CreateExperiment()
        data = (
            (finder._reagent(Reagent.make_hash('Eco63',Concentration.value_from_quotient(1, 0.4))),  ('A', 'H', 5, 5)),
            (finder._reagent(Reagent.make_hash('Eco60', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 5, 5)),
            (finder._reagent(Reagent.make_hash('Efs04', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 6, 6)),
            (finder._reagent(Reagent.make_hash('Efs01', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 6, 6)),
            (finder._reagent(Reagent.make_hash('van10', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 7, 7)),
            (finder._reagent(Reagent.make_hash('van06', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 7, 7)),
            (finder._reagent(Reagent.make_hash('van05', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 8, 8)),
            (finder._reagent(Reagent.make_hash('van01',Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 8, 8)),
            (finder._reagent(Reagent.make_hash('Spo09', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 8, 8)),
            (finder._reagent(Reagent.make_hash('Spo13', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 8, 8)),

        )
        return experiment._rules_from_data('PA Primers', data)

    def _id_primers_rules_1(self):
        # Distribution in English.
        # One block repeating every 4 columns, for all rows.
        finder = Finders()
        experiment = CreateExperiment()
        data = (
            (finder._reagent(Reagent.make_hash('Eco64', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 1, 3)),
            (finder._reagent(Reagent.make_hash('Eco66', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 1, 3)),
            (finder._reagent(Reagent.make_hash('Efs03', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 3, 6)),
            (finder._reagent(Reagent.make_hash('Efs02', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 3, 6)),
            (finder._reagent(Reagent.make_hash('van30', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 6, 9)),
            (finder._reagent(Reagent.make_hash('van33', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 6, 9)),
            (finder._reagent(Reagent.make_hash('van04', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 9, 12)),
            (finder._reagent(Reagent.make_hash('van01', Concentration.value_from_quotient(1, 0.4))), ('A', 'H', 9, 12)),
        )
        return experiment._rules_from_data('ID-Primers', data)





if __name__ == "__main__":
    ReferenceExperiment().create()

