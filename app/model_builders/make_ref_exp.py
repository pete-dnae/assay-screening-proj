"""
Creates and stores a reference experiment in the database.
"""

from app.models import Arg
from app.models import Concentration
from app.models import ConcreteReagent
from app.models import Gene
from app.models import Organism
from app.models import Primer
from app.models import PrimerPair
from app.models import Strain


class ReferenceExperiment():

    def __init__(self):
        self._create_shared_entities() # Organisms, Stock reagents etc.
        self._create_experiment_specific_entities() # Plate allocations etc.

    def create(self):
        return None

    #-----------------------------------------------------------------------
    # Private below.
    #-----------------------------------------------------------------------

    def _create_shared_entities(self):
        self._create_concrete_reagents()
        self._create_organisms_and_strains()
        self._create_genes_and_primers()

    def _create_experiment_specific_entities(self):
        pass

    def _create_concrete_reagents(self):
        self._create_concrete_reagent('BSA', '-', 20, 1, 'mg/ml')
        self._create_concrete_reagent('DNA Free Water', '22884100', 0, 0, 'X')
        self._create_concrete_reagent('dNTPs', '-', 10, 0.2, 'mM each')
        self._create_concrete_reagent('KCl', '-', 1000, 48, 'mM')
        self._create_concrete_reagent('KOH', '-', 100, 1, 'mM')
        self._create_concrete_reagent('MgCl2', '449890', 25, 2.06, 'mM')
        self._create_concrete_reagent('Titanium PCR Buffer', '1602046A', 
            10, 0.13, 'X')
        self._create_concrete_reagent('SYBRgreen', '-', 100, 0.32, 'X')
        self._create_concrete_reagent('Titanium Taq', '1607230A', 50, 1.0, 'x')
        self._create_concrete_reagent('Titanium Taq', '1607230A', 50, 1.3, 'x')
        self._create_concrete_reagent('Triton', '-', 10, 0.04, '%')


    def _create_concrete_reagent(self, name, lot, stock, final, units):
        concentration = Concentration.objects.create(
            stock=stock, final=final, units=units)
        reagent = ConcreteReagent.objects.create(
            name=name, lot=lot, concentration=concentration)
        return reagent


    def _create_organisms_and_strains(self):
        self._create_organisms()
        self._create_args()
        self._create_strains()

    def _create_organisms(self):
        Organism.objects.create(
            abbreviation='Eco', full_name='Escherichia coli')
        Organism.objects.create(
            abbreviation='Efm', full_name='Enterococcus faecium')
        Organism.objects.create(
            abbreviation='Efs', full_name='Enterococcus faecalis')
        Organism.objects.create(
            abbreviation='Kox', full_name='Klebsiella oxytoca')
        Organism.objects.create(
            abbreviation='Kpn', full_name='Klebsiella pneumoniae')
        Organism.objects.create(
            abbreviation='Pmi', full_name='Proteus mirabilis')
        Organism.objects.create(
            abbreviation='Spo', full_name='Schizosaccharomyces pombe')

    def _create_args(self):
        Arg.objects.create(name='CTX-M9 TEM-WT')
        Arg.objects.create(name='KPC')
        Arg.objects.create(name='vanA')
        Arg.objects.create(name='vanB')

    def _create_strains(self):
        self._create_strain('ATCC 15764', 'Kox', None, 6684900)
        self._create_strain('ATCC 26189', 'Spo', None, 12570000)
        self._create_strain('ATCC 700802', 'Efs', 'vanB', 3220000)
        self._create_strain('ATCC BAA-1705', 'Kpn', 'KPC', 5300000)
        self._create_strain('ATCC BAA-2317', 'Efm', 'vanA', 2698130)
        self._create_strain('ATCC BAA-2355', 'Eco', 'vanA', 4600000)
        self._create_strain('ATCC BAA-633', 'Pmi', None, 4063000)

    def _create_strain(self, strain_name, organism_abbreviation, 
            arg_name, genome_size):
        organism = Organism.objects.get(abbreviation=organism_abbreviation)
        arg = Arg.objects.get(name=arg_name) if arg_name else None
        Strain.objects.create(name=strain_name, organism=organism, 
            arg=arg, genome_size=genome_size)
        
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

        self._create_primer('Eco', 'Eco63', 'fwd', 'uidA')
        self._create_primer('Eco', 'Eco60', 'rev', 'uidA')
        self._create_primer('Eco', 'Eco64', 'fwd', 'uidA')
        self._create_primer('Eco', 'Eco66', 'rev', 'uidA')

        self._create_primer('Efm', 'van05', 'fwd', 'vanA')
        self._create_primer('Efm', 'van01', 'rev', 'vanA')
        self._create_primer('Efm', 'van04', 'fwd', 'vanA')
        self._create_primer('Efm', 'van02', 'rev', 'vanA')

        self._create_primer('Efs', 'Efs04', 'fwd', 'cpn60')
        self._create_primer('Efs', 'Efs01', 'rev', 'cpn60')
        self._create_primer('Efs', 'Efs03', 'fwd', 'cpn60')
        self._create_primer('Efs', 'Efs02', 'rev', 'cpn60')

        self._create_primer('Efs', 'van10', 'fwd', 'vanB')
        self._create_primer('Efs', 'van06', 'rev', 'vanB')
        self._create_primer('Efs', 'van30', 'fwd', 'vanB')
        self._create_primer('Efs', 'van33', 'rev', 'vanB')

        self._create_primer('Kox', 'Kox05', 'fwd', 'peh')
        self._create_primer('Kox', 'Kox02', 'rev', 'peh')
        self._create_primer('Kox', 'Kox04', 'fwd', 'peh')
        self._create_primer('Kox', 'Kox03', 'rev', 'peh')

        self._create_primer('Kpn', 'Kpn13', 'fwd', 'khe')
        self._create_primer('Kpn', 'Kpn01', 'rev', 'khe')
        self._create_primer('Kpn', 'Kpn03', 'fwd', 'khe')
        self._create_primer('Kpn', 'Kpn02', 'rev', 'khe')

        self._create_primer('Pmi', 'Pmi01', 'fwd', 'zapA')
        self._create_primer('Pmi', 'Pmi05', 'rev', 'zapA')
        self._create_primer('Pmi', 'Pmi02', 'fwd', 'zapA')
        self._create_primer('Pmi', 'Pmi03', 'rev', 'zapA')

        self._create_primer('Spo', 'Spo09', 'fwd', 'gp')
        self._create_primer('Spo', 'Spo13', 'rev', 'gp')
        self._create_primer('Spo', 'Spo03', 'fwd', 'gp')
        self._create_primer('Spo', 'Spo05', 'rev', 'gp')

    def _create_primer(self, organism, primer_name, fwd_or_rev, gene):
        Primer.objects.create(
            oligo_code=organism,
            full_name=primer_name,
            role=fwd_or_rev,
            organism=Organism.objects.get(abbreviation=organism),
            gene=Gene.objects.get(name=gene),
        )

    def _create_primer_pairs(self):
        self._create_primer_pair('Eco63', 'Eco60', True, False)
        self._create_primer_pair('Efs04', 'Efs01', True, False)
        self._create_primer_pair('van10', 'van06', True, False)
        self._create_primer_pair('van05', 'van01', True, False)
        self._create_primer_pair('Kox05', 'Kox02', True, False)
        self._create_primer_pair('Kpn13', 'Kpn01', True, False)
        self._create_primer_pair('Pmi01', 'Pmi05', True, False)
        self._create_primer_pair('Spo09', 'Spo13', True, False)

        self._create_primer_pair('Eco64', 'Eco66', False, True)
        self._create_primer_pair('Efs03', 'Efs02', False, True)
        self._create_primer_pair('van30', 'van33', False, True)
        self._create_primer_pair('van04', 'van02', False, True)
        self._create_primer_pair('Kox04', 'Kox03', False, True)
        self._create_primer_pair('Kpn03', 'Kpn02', False, True)
        self._create_primer_pair('Pmi03', 'Pmi02', False, True)
        self._create_primer_pair('Spo03', 'Spo05', False, True)

    def _create_primer_pair(self, fwd_name, rev_name, for_pa, for_id):
        PrimerPair.objects.create(
            forward_primer = Primer.objects.get(full_name=fwd_name),
            reverse_primer = Primer.objects.get(full_name=rev_name),
            suitable_for_pa = for_pa,
            suitable_for_id = for_id,
        )
        

