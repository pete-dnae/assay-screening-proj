"""
Creates the minimum viable starter content for a virgin database.
For example primers, strains etc. Then a reference experiement..
"""

from app.models.strain_models import *
from app.models.experiment_model import *
from app.models.rule_models import *
from .finders import Finders
from app.model_builders.common_modules import CommonModules


class ReferenceExperiment():
    """
    Creates all the database entities required to assemble an example,
    refrence models.Experiment, and returns the correpsonding instance.
    """

    def __init__(self):
        self.experiment = None

    def create(self):
        self._create_shared_entities()  # Organisms, Stock reagents etc.
        self.experiment = self._create_experiment()
        return self.experiment

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _sample_rule_script(self):
        return "V 1 \n" \
               "P1 \n" \
               "A DNA-free-Water            1-12    A-H 3.35 x \n" \
               "A Titanium-PCR-Buffer       1-12    A-H 0.63 x \n" \
               "A KCl                       1-12    A-H 2.40 mM \n" \
               "A MgCl2                     1-12    A-H 4.13 mM \n" \
               "A BSA                       1-12    A-H 2.5 mg/ml \n" \
               "A dNTPs                     1-12    A-H 1.00 mMeach \n" \
               "A Titanium-Taq              1-12    A-H 1.00 x \n" \
               "A (Eco)-ATCC-BAA-2355       1,5,9   A-B   0 copies \n" \
               "A (Eco)-ATCC-BAA-2355       1,5     C-H   5 copies \n" \
               "A (Eco)-ATCC-BAA-2355       9       C-D   50 copies \n" \
               "A (Eco)-ATCC-BAA-2355       9       E-F   500 copies \n" \
               "A (Eco)-ATCC-BAA-2355       9       G-H   5000 copies \n" \
               "A (Efs-vanB)-ATCC-700802    2,6,10  A-B   0 copies \n" \
               "A (Efs-vanB)-ATCC-700802    2,6     C-H   5 copies \n" \
               "A (Efs-vanB)-ATCC-700802    10      C-D   50 copies \n" \
               "A (Efs-vanB)-ATCC-700802    10      E-F   500 copies \n" \
               "A (Efs-vanB)-ATCC-700802    10      G-H   5000 copies \n" \
               "A (Efs-vanB)-ATCC-700802    3,7,11  A-B   0 copies \n" \
               "A (Efs-vanB)-ATCC-700802    3,7     C-H   5 copies \n" \
               "A (Efs-vanB)-ATCC-700802    11      C-D   50 copies \n" \
               "A (Efs-vanB)-ATCC-700802    11      E-F   500 copies \n" \
               "A (Efs-vanB)-ATCC-700802    11      G-H   5000 copies \n" \
               "A (Kox)-ATCC-15764          4,8,12  A-B   0 copies \n" \
               "A (Kox)-ATCC-15764          4,8     C-H   5 copies \n" \
               "A (Kox)-ATCC-15764          12      C-D   50 copies \n" \
               "A (Kox)-ATCC-15764          12      E-F   500 copies \n" \
               "A (Kox)-ATCC-15764          12      G-H   5000 copies \n" \
               "A Ec_uidA_6.x_Eco63_Eco60   1-4     A-H   0.4 uM \n" \
               "A Efs_cpn60_1.x_Efs04_Efs01 1-4     A-H   0.4 uM \n" \
               "A Efs_vanB_1.x_van10_van06  1-4     A-H   0.4 uM \n" \
               "A Efm_vanA_1.x_van05_van01  1-4     A-H   0.4 uM \n" \
               "A Ko_pehX_1.x_Kox05_Kox02   1-4     A-H   0.4 uM \n" \
               "A Kp_khe_2.x_Kpn13_Kpn01    1-4     A-H   0.4 uM \n" \
               "A Pm_zapA_1.x_Pmi01_Pmi05   1-4     A-H   0.4 uM \n" \
               "A Spo_gp_1.x_Spo09_Spo13    1-4     A-H   0.4 uM \n" \
               "A Ec_uidA_6.x_Eco63_Eco60   5       A-H   0.4 uM \n" \
               "A Efs_cpn60_1.x_Efs04_Efs01 6       A-H   0.4 uM \n" \
               "A Efs_vanB_1.x_van10_van06  7       A-H   0.4 uM \n" \
               "A Efm_vanA_1.x_van05_van01  8       A-H   0.4 uM \n" \
               "A HgDna                     1-8     E-H   3000 ng \n" \
               "A HgDna                     1-8     B     3000 ng \n"


    def _create_shared_entities(self):
        self._create_organisms_and_strains()
        self._create_genes_and_primers()
        self._create_reagents()

    def _create_reagents(self):

        ConcreteReagent.make('BSA', '-', 20, 1, 'mg/ml')
        ConcreteReagent.make('DNA-Free-Water', '22884100', 1, 1, 'x')
        ConcreteReagent.make('dNTPs', '-', 10, 0.2, 'mM')
        ConcreteReagent.make('KCl', '-', 1000, 48, 'mM')
        ConcreteReagent.make('KOH', '-', 100, 1, 'mM')
        ConcreteReagent.make('MgCl2', '449890', 25, 2.06, 'mM')
        ConcreteReagent.make('Titanium-PCR-Buffer', '1602046A',
                             10, 0.13, 'X')
        ConcreteReagent.make('SYBRgreen', '-', 100, 0.32, 'x')
        ConcreteReagent.make('Titanium-Taq', '1607230A', 50, 1.0, 'x')
        ConcreteReagent.make('Titanium-Taq', '1607230A', 50, 1.3, 'x')
        ConcreteReagent.make('Triton', '-', 10, 0.04, '%')
        for count in (0, 5000):
            # TODO this is not the correct concentration value.
            ConcreteReagent.make('HgDna', '-', 1, count, 'ng/ul')

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
                ('ATCC BAA-2355', 'Eco', 'CTX-M9 TEM-WT', 4600000),
                ('ATCC 26189', 'Spo', None, 12570000),
                ('ATCC 700802', 'Efs', 'vanB', 3220000),
                ('ATCC 15764', 'Kpn', 'KPC', 6684900),
                ('ATCC BAA-2317', 'Efm', 'vanA', 2698130),
                ('ATCC BAA-633', 'Pmi', None, 4063000)):
            arg = None if arg_name is None else finder.arg(arg_name)
            Strain.make(strain_name, finder.org(org_name), arg, genome_len)

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
        finder = Finders()
        for organism_name, primer_name, role, gene_name in (
                ('Eco', 'Eco63', 'fwd', 'uidA'), ('Eco', 'Eco60', 'rev', 'uidA'),
                ('Eco', 'Eco64', 'fwd', 'uidA'), ('Eco', 'Eco66', 'rev', 'uidA'),
                ('Efm', 'van05', 'fwd', 'vanA'), ('Efm', 'van01', 'rev', 'vanA'),
                ('Efm', 'van04', 'fwd', 'vanA'), ('Efm', 'van02', 'rev', 'vanA'),
                ('Efs', 'Efs04', 'fwd', 'cpn60'), ('Efs', 'Efs01', 'rev', 'cpn60'),
                ('Efs', 'Efs03', 'fwd', 'cpn60'), ('Efs', 'Efs02', 'rev', 'cpn60'),
                ('Efs', 'van10', 'fwd', 'vanB'), ('Efs', 'van06', 'rev', 'vanB'),
                ('Efs', 'van30', 'fwd', 'vanB'), ('Efs', 'van33', 'rev', 'vanB'),
                ('Kox', 'Kox05', 'fwd', 'peh'), ('Kox', 'Kox02', 'rev', 'peh'),
                ('Kox', 'Kox04', 'fwd', 'peh'), ('Kox', 'Kox03', 'rev', 'peh'),
                ('Kpn', 'Kpn13', 'fwd', 'khe'), ('Kpn', 'Kpn01', 'rev', 'khe'),
                ('Kpn', 'Kpn03', 'fwd', 'khe'), ('Kpn', 'Kpn02', 'rev', 'khe'),
                ('Pmi', 'Pmi01', 'fwd', 'zapA'), ('Pmi', 'Pmi05', 'rev', 'zapA'),
                ('Pmi', 'Pmi02', 'fwd', 'zapA'), ('Pmi', 'Pmi03', 'rev', 'zapA'),
                ('Spo', 'Spo09', 'fwd', 'gp'), ('Spo', 'Spo13', 'rev', 'gp'),
                ('Spo', 'Spo03', 'fwd', 'gp'), ('Spo', 'Spo05', 'rev', 'gp')):
            Primer.make(finder.org(organism_name), primer_name, role, finder.gene(gene_name))

    def _create_primer_pairs(self):
        finder = Finders()
        PrimerPair.make(finder.prim('Eco63'), finder.prim('Eco60'), True, False)
        PrimerPair.make(finder.prim('Efs04'), finder.prim('Efs01'), True, False)
        PrimerPair.make(finder.prim('van10'), finder.prim('van06'), True, False)
        PrimerPair.make(finder.prim('van05'), finder.prim('van01'), True, False)
        PrimerPair.make(finder.prim('Kox05'), finder.prim('Kox02'), True, False)
        PrimerPair.make(finder.prim('Kpn13'), finder.prim('Kpn01'), True, False)
        PrimerPair.make(finder.prim('Pmi01'), finder.prim('Pmi05'), True, False)
        PrimerPair.make(finder.prim('Spo09'), finder.prim('Spo13'), True, False)

        PrimerPair.make(finder.prim('Eco64'), finder.prim('Eco66'), False, True)
        PrimerPair.make(finder.prim('Efs03'), finder.prim('Efs02'), False, True)
        PrimerPair.make(finder.prim('van30'), finder.prim('van33'), False, True)
        PrimerPair.make(finder.prim('van04'), finder.prim('van02'), False, True)
        PrimerPair.make(finder.prim('Kox04'), finder.prim('Kox03'), False, True)
        PrimerPair.make(finder.prim('Kpn03'), finder.prim('Kpn02'), False, True)
        PrimerPair.make(finder.prim('Pmi02'), finder.prim('Pmi03'), False, True)
        PrimerPair.make(finder.prim('Spo03'), finder.prim('Spo05'), False, True)

    def _create_experiment(self):
        cm = CommonModules()
        cm.validate_rules(self._sample_rule_script())
        return Experiment.make(
            'reference_experiment_1',
            'PH',
            RuleScript.make(self._sample_rule_script()),
            cm.create_pa_cycling(),
            cm.create_id_cycling(),
        )


if __name__ == "__main__":
    ReferenceExperiment().create()
