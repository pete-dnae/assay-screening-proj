"""
Creates and stores a reference experiment in the database.
"""

from app.models import Arg
from app.models import BufferMix
from app.models import Concentration
from app.models import ConcreteReagent
from app.models import Experiment
from app.models import Gene
from app.models import MasterMix
from app.models import MixedReagent
from app.models import Organism
from app.models import PlaceholderReagent
from app.models import Primer
from app.models import PrimerKit
from app.models import PrimerPair
from app.models import Strain
from app.models import StrainKit


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
        self._create_concrete_reagents()
        self._create_organisms_and_strains()
        self._create_genes_and_primers()

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
        concentration = self._make_concentration(stock, final, units)
        reagent = ConcreteReagent.objects.create(
            name=name, lot=lot, concentration=concentration)
        return reagent

    def _make_concentration(self, stock, final, units):
        return Concentration.objects.create(
            stock=stock, final=final, units=units)


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
        self._create_primer_pair('Pmi02', 'Pmi03', False, True)
        self._create_primer_pair('Spo03', 'Spo05', False, True)

    def _create_primer_pair(self, fwd_name, rev_name, for_pa, for_id):
        PrimerPair.objects.create(
            forward_primer = Primer.objects.get(full_name=fwd_name),
            reverse_primer = Primer.objects.get(full_name=rev_name),
            suitable_for_pa = for_pa,
            suitable_for_id = for_id,
        )


    def _create_experiment(self):
        exp = Experiment.objects.create(
            experiment_name='reference_experiment_1',
            designer_name='PH',
            pa_mastermix=self._create_pa_mastermix(),
            id_mastermix=self._create_id_mastermix(),
            primer_kit=self._create_primer_kit(),
            strain_kit = self._create_strain_kit(),
            pa_cycling = self._create_pa_cycling(),
            id_cycling = self._create_id_cycling(),
        )
        exp.plates.add(self._create_slide_1())
        exp.plates.add(self._create_slide_2())

        exp.save()
        return exp

    def _create_pa_mastermix(self):
        mastermix = MasterMix.objects.create(
            final_volume=50,
            water=ConcreteReagent.objects.get(
                name='DNA Free Water'),
            buffer_mix=MixedReagent.objects.create(
                buffer_mix= self._create_pa_buffermix(),
                concentration = self._make_concentration(3.3, 1, 'X'),
            ),
            primers=self._create_placeholder_reagent(
                'Primers', 10, 0.4, 'uM each'),
            hgDNA=self._create_placeholder_reagent(
                'HgDNA', 120, 60, 'ng/ul'),
            template=self._create_placeholder_reagent(
                'Template', 1, 0.1, 'cp/ul'),
        )
        return mastermix

    def _create_id_mastermix(self):
        mastermix = MasterMix.objects.create(
            final_volume=20,
            water=ConcreteReagent.objects.get(
                name='DNA Free Water'),
            buffer_mix=MixedReagent.objects.create(
                buffer_mix= self._create_id_buffermix(),
                concentration = self._make_concentration(2, 1, 'X'),
            ),
            primers=self._create_placeholder_reagent(
                'Primers', 10, 0.4, 'uM each'),
            hgDNA=None,
            template=self._create_placeholder_reagent(
                'Template', 10, 2.5, 'cp/ul'),
        )
        return mastermix


    def _create_pa_buffermix(self):
        buffermix = BufferMix.objects.create(
            volume=15,
            final_volume=50,
        )
        for name in ('DNA Free Water', 'Titanium PCR Buffer', 'KCl', 'MgCl2',
                'BSA', 'dNTPs'):
            reagent = ConcreteReagent.objects.get(name=name)
            buffermix.concrete_reagents.add(reagent)
        # Taq requires additional disambiguation.
        taq = ConcreteReagent.objects.get(
            name='Titanium Taq', concentration__final=1.00)
        buffermix.concrete_reagents.add(taq)

        buffermix.save()
        return buffermix

    def _create_id_buffermix(self):
        buffermix = BufferMix.objects.create(
            volume=10,
            final_volume=20,
        )
        for name in ('DNA Free Water', 'KCl', 'MgCl2', 'BSA', 
                'Triton', 'SYBRgreen', 'dNTPs', 'KOH'):
            reagent = ConcreteReagent.objects.get(name=name)
            buffermix.concrete_reagents.add(reagent)
        # Taq requires additional disambiguation.
        taq = ConcreteReagent.objects.get(
            name='Titanium Taq', concentration__final=1.3)
        buffermix.concrete_reagents.add(taq)

        buffermix.save()
        return buffermix


    def _create_placeholder_reagent(self, placeholder_type, 
            stock, final, units):
        return PlaceholderReagent.objects.create(
            type=placeholder_type,
            concentration=self._make_concentration(stock, final, units)
        )

    def _create_primer_kit(self):
        kit = PrimerKit.objects.create(
            fwd_concentration=self._make_concentration(10, 0.4, 'uM'),
            rev_concentration=self._make_concentration(10, 0.4, 'uM'),
        )
        self._add_pa_primers_to_kit(kit.pa_primers)
        self._add_id_primers_to_kit(kit.id_primers)
        kit.save()
        return kit

    def _add_pa_primers_to_kit(self, m2m_field):
        f = m2m_field
        pa = True
        id = False
        f.add(self._find_primer_pair('Eco63', 'Eco60', pa, id))
        f.add(self._find_primer_pair('Efs04', 'Efs01', pa, id))
        f.add(self._find_primer_pair('van10', 'van06', pa, id))
        f.add(self._find_primer_pair('van05', 'van01', pa, id))
        f.add(self._find_primer_pair('Kox05', 'Kox02', pa, id))
        f.add(self._find_primer_pair('Kpn13', 'Kpn01', pa, id))
        f.add(self._find_primer_pair('Pmi01', 'Pmi05', pa, id))
        f.add(self._find_primer_pair('Spo09', 'Spo13', pa, id))

    def _add_id_primers_to_kit(self, m2m_field):
        f = m2m_field
        pa = False
        id = True
        f.add(self._find_primer_pair('Eco64', 'Eco66', pa, id))
        f.add(self._find_primer_pair('Efs03', 'Efs02', pa, id))
        f.add(self._find_primer_pair('van30', 'van33', pa, id))
        f.add(self._find_primer_pair('van04', 'van02', pa, id))
        f.add(self._find_primer_pair('Kox04', 'Kox03', pa, id))
        f.add(self._find_primer_pair('Kpn03', 'Kpn02', pa, id))
        f.add(self._find_primer_pair('Pmi02', 'Pmi03', pa, id))
        f.add(self._find_primer_pair('Spo03', 'Spo05', pa, id))

    def _find_primer_pair(self, fwd_name, rev_name, 
            suitable_for_pa, suitable_for_id):
        print('XXXX %s %s' % (fwd_name, rev_name))
        primer_pair = PrimerPair.objects.get(
            forward_primer__full_name=fwd_name,
            reverse_primer__full_name=rev_name,
            suitable_for_pa=suitable_for_pa,
            suitable_for_id=suitable_for_id,
            )
        return primer_pair

    def _strains_kit(self):
        got to here
