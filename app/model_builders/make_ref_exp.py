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
        self._create_concrete_reagents()
        self._create_organisms_and_strains()
        self._create_genes_and_primers()

    def _create_concrete_reagents(self):
        ConcreteReagent.make('BSA', '-', 20, 1, 'mg/ml')
        ConcreteReagent.make('DNA Free Water', '22884100', 0, 0, 'X')
        ConcreteReagent.make('dNTPs', '-', 10, 0.2, 'mM each')
        ConcreteReagent.make('KCl', '-', 1000, 48, 'mM')
        ConcreteReagent.make('KOH', '-', 100, 1, 'mM')
        ConcreteReagent.make('MgCl2', '449890', 25, 2.06, 'mM')
        ConcreteReagent.make('Titanium PCR Buffer', '1602046A', 
            10, 0.13, 'X')
        ConcreteReagent.make('SYBRgreen', '-', 100, 0.32, 'X')
        ConcreteReagent.make('Titanium Taq', '1607230A', 50, 1.0, 'x')
        ConcreteReagent.make('Titanium Taq', '1607230A', 50, 1.3, 'x')
        ConcreteReagent.make('Triton', '-', 10, 0.04, '%')


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
        Strain.make('ATCC 15764', 'Kox', None, 6684900)
        Strain.make('ATCC 26189', 'Spo', None, 12570000)
        Strain.make('ATCC 700802', 'Efs', 'vanB', 3220000)
        Strain.make('ATCC BAA-1705', 'Kpn', 'KPC', 5300000)
        Strain.make('ATCC BAA-2317', 'Efm', 'vanA', 2698130)
        Strain.make('ATCC BAA-2355', 'Eco', 'vanA', 4600000)
        Strain.make('ATCC BAA-633', 'Pmi', None, 4063000)

        
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

        Primer.make('Eco', 'Eco63', 'fwd', 'uidA')
        Primer.make('Eco', 'Eco60', 'rev', 'uidA')
        Primer.make('Eco', 'Eco64', 'fwd', 'uidA')
        Primer.make('Eco', 'Eco66', 'rev', 'uidA')

        Primer.make('Efm', 'van05', 'fwd', 'vanA')
        Primer.make('Efm', 'van01', 'rev', 'vanA')
        Primer.make('Efm', 'van04', 'fwd', 'vanA')
        Primer.make('Efm', 'van02', 'rev', 'vanA')

        Primer.make('Efs', 'Efs04', 'fwd', 'cpn60')
        Primer.make('Efs', 'Efs01', 'rev', 'cpn60')
        Primer.make('Efs', 'Efs03', 'fwd', 'cpn60')
        Primer.make('Efs', 'Efs02', 'rev', 'cpn60')

        Primer.make('Efs', 'van10', 'fwd', 'vanB')
        Primer.make('Efs', 'van06', 'rev', 'vanB')
        Primer.make('Efs', 'van30', 'fwd', 'vanB')
        Primer.make('Efs', 'van33', 'rev', 'vanB')

        Primer.make('Kox', 'Kox05', 'fwd', 'peh')
        Primer.make('Kox', 'Kox02', 'rev', 'peh')
        Primer.make('Kox', 'Kox04', 'fwd', 'peh')
        Primer.make('Kox', 'Kox03', 'rev', 'peh')

        Primer.make('Kpn', 'Kpn13', 'fwd', 'khe')
        Primer.make('Kpn', 'Kpn01', 'rev', 'khe')
        Primer.make('Kpn', 'Kpn03', 'fwd', 'khe')
        Primer.make('Kpn', 'Kpn02', 'rev', 'khe')

        Primer.make('Pmi', 'Pmi01', 'fwd', 'zapA')
        Primer.make('Pmi', 'Pmi05', 'rev', 'zapA')
        Primer.make('Pmi', 'Pmi02', 'fwd', 'zapA')
        Primer.make('Pmi', 'Pmi03', 'rev', 'zapA')

        Primer.make('Spo', 'Spo09', 'fwd', 'gp')
        Primer.make('Spo', 'Spo13', 'rev', 'gp')
        Primer.make('Spo', 'Spo03', 'fwd', 'gp')
        Primer.make('Spo', 'Spo05', 'rev', 'gp')

    def _create_primer_pairs(self):
        PrimerPair.make('Eco63', 'Eco60', True, False)
        PrimerPair.make('Efs04', 'Efs01', True, False)
        PrimerPair.make('van10', 'van06', True, False)
        PrimerPair.make('van05', 'van01', True, False)
        PrimerPair.make('Kox05', 'Kox02', True, False)
        PrimerPair.make('Kpn13', 'Kpn01', True, False)
        PrimerPair.make('Pmi01', 'Pmi05', True, False)
        PrimerPair.make('Spo09', 'Spo13', True, False)

        PrimerPair.make('Eco64', 'Eco66', False, True)
        PrimerPair.make('Efs03', 'Efs02', False, True)
        PrimerPair.make('van30', 'van33', False, True)
        PrimerPair.make('van04', 'van02', False, True)
        PrimerPair.make('Kox04', 'Kox03', False, True)
        PrimerPair.make('Kpn03', 'Kpn02', False, True)
        PrimerPair.make('Pmi02', 'Pmi03', False, True)
        PrimerPair.make('Spo03', 'Spo05', False, True)


    def _create_experiment(self):
        _EXPERIMENT_NAME = 'reference_experiment_1'
        exp = Experiment.objects.create(
            experiment_name=_EXPERIMENT_NAME,
            designer_name='PH',
            pa_mastermix=self._create_pa_mastermix(),
            id_mastermix=self._create_id_mastermix(),
            primer_kit=self._create_primer_kit(),
            strain_kit = self._create_strain_kit(),
            pa_cycling = self._create_pa_cycling(),
            id_cycling = self._create_id_cycling(),
        )
        exp.plates.add(self._create_plate_1('plate_1'))
        #exp.plates.add(self._create_plate_2('plate_2'))

        exp.save()
        return exp

    def _create_pa_mastermix(self):
        mastermix = MasterMix.objects.create(
            final_volume=50,
            water=ConcreteReagent.objects.get(
                name='DNA Free Water'),
            buffer_mix=MixedReagent.objects.create(
                buffer_mix= self._create_pa_buffermix(),
                concentration = Concentration.make(3.3, 1, 'X'),
            ),
            primers=PlaceholderReagent.make(
                'Primers', 10, 0.4, 'uM each'),
            hgDNA=PlaceholderReagent.make(
                'HgDNA', 120, 60, 'ng/ul'),
            template=PlaceholderReagent.make(
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
                concentration = Concentration.make(2, 1, 'X'),
            ),
            primers=PlaceholderReagent.make(
                'Primers', 10, 0.4, 'uM each'),
            hgDNA=None,
            template=PlaceholderReagent.make(
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


    def _create_primer_kit(self):
        kit = PrimerKit.objects.create(
            fwd_concentration=Concentration.make(10, 0.4, 'uM'),
            rev_concentration=Concentration.make(10, 0.4, 'uM'),
        )
        self._add_pa_primers_to_kit(kit.pa_primers)
        self._add_id_primers_to_kit(kit.id_primers)
        kit.save()
        return kit

    def _add_pa_primers_to_kit(self, m2m_field):
        f = m2m_field
        f.add(self._find_pa_primer_pair('Eco63', 'Eco60'))
        f.add(self._find_pa_primer_pair('Efs04', 'Efs01'))
        f.add(self._find_pa_primer_pair('van10', 'van06'))
        f.add(self._find_pa_primer_pair('van05', 'van01'))
        f.add(self._find_pa_primer_pair('Kox05', 'Kox02'))
        f.add(self._find_pa_primer_pair('Kpn13', 'Kpn01'))
        f.add(self._find_pa_primer_pair('Pmi01', 'Pmi05'))
        f.add(self._find_pa_primer_pair('Spo09', 'Spo13'))

    def _add_id_primers_to_kit(self, m2m_field):
        f = m2m_field
        pa = False
        id = True
        f.add(self._find_id_primer_pair('Eco64', 'Eco66'))
        f.add(self._find_id_primer_pair('Efs03', 'Efs02'))
        f.add(self._find_id_primer_pair('van30', 'van33'))
        f.add(self._find_id_primer_pair('van04', 'van02'))
        f.add(self._find_id_primer_pair('Kox04', 'Kox03'))
        f.add(self._find_id_primer_pair('Kpn03', 'Kpn02'))
        f.add(self._find_id_primer_pair('Pmi02', 'Pmi03'))
        f.add(self._find_id_primer_pair('Spo03', 'Spo05'))

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

    def _create_strain_kit(self):
        kit = StrainKit.objects.create()

        kit.strains.add(Strain.objects.get(name='ATCC 15764'))
        kit.strains.add(Strain.objects.get(name='ATCC 15764'))
        kit.strains.add(Strain.objects.get(name='ATCC 26189'))
        kit.strains.add(Strain.objects.get(name='ATCC 700802'))
        kit.strains.add(Strain.objects.get(name='ATCC BAA-1705'))
        kit.strains.add(Strain.objects.get(name='ATCC BAA-2317'))
        kit.strains.add(Strain.objects.get(name='ATCC BAA-2355'))
        kit.strains.add(Strain.objects.get(name='ATCC BAA-633'))
        kit.strains.add(Strain.objects.get(name='ATCC BAA-633'))

        kit.save()
        return kit

    def _create_pa_cycling(self):
        return CyclingPattern.objects.create(
            activation_time=120,
            activation_temp=95,
            num_cycles=20,
            denature_time=10,
            denature_temp=95,
            anneal_time=10,
            anneal_temp=62,
            extend_temp=72,
            extend_time=30,
        )

    def _create_id_cycling(self):
        return CyclingPattern.objects.create(
            activation_time=120,
            activation_temp=95,
            num_cycles=20,
            denature_time=10,
            denature_temp=95,
            anneal_time=0,
            anneal_temp=0,
            extend_temp=62,
            extend_time=25,
        )

    def _create_plate_1(self, experiment_name):
        plate = Plate.objects.create(
            name=('%s_1' % experiment_name),
            allocation_instructions=self._make_allocation_1(),
        )
        return plate

    def _make_allocation_1(self):

        alloc = AllocationInstructions.objects.create(
            suppressed_columns='4, 8, 12',
            rule_list=RuleList.objects.create(),
        )

        m2m = alloc.rule_list.rules
        
        self._add_strains_rules_1(m2m)
        self._add_strains_copies_rules_1(m2m)
        self._add_hg_dna_rules_1(m2m)
        self._add_pa_primers_rules_1(m2m)
        self._add_dilution_factor_rules_1(m2m)
        self._add_id_primers_rules_1(m2m)

        alloc.save()
        return alloc

    def _add_strains_rules_1(self, m2m_field):
        # Same pattern repeated every 4 columns, same for all rows.
        data = (
            (
                'ATCC BAA-2355, ATCC 700802, ATCC 700802, ATCC 15764',
                'In Blocks',
                ('A', 'H', 1, 12),
            ),
        )
        self._add_rules_from_data(m2m_field, 'Strain', data)

    def _add_strains_copies_rules_1(self, m2m_field):
        # Blanket fill with 5's everwhere first
        # Then, first two rows - filled with zeros.
        # Then, larger numbers in small zones.
        data = (
            ('5', 'Consecutive', ('A', 'H', 1, 12)),
            ('0', 'Consecutive', ('A', 'B', 1, 12)),
            ('50', 'Consecutive', ('C', 'D', 9, 12)),
            ('500', 'Consecutive', ('E', 'F', 9, 12)),
            ('5000', 'Consecutive', ('G', 'H', 9, 12)),
        )
        self._add_rules_from_data(m2m_field,
            'Strain Count', data)


    def _add_hg_dna_rules_1(self, m2m_field):
        # Distribution in English.
        # Blanket fill with 0 everywhere.
        # Then 3000 in a bottom left block.
        data = (
            ('0', 'Consecutive', ('A', 'H', 1, 12)),
            ('5000', 'Consecutive', ('F', 'H', 1, 8)),
        )
        self._add_rules_from_data(m2m_field, 'HgDNA', data)

    def _add_pa_primers_rules_1(self, m2m_field):
        # Distribution in English.
        # Columns split into 3 groups, each with its own block allocation.
        # Uniform for all rows.

        primer_block = 'Eco63 Eco60, Efs04 Efs01, van10 van06, van05 van01'

        data = (
            ('poolB1', 'Consecutive', ('A', 'H', 1, 4)),
            (primer_block, 'Consecutive', ('A', 'H', 5, 8)),
            ('', 'Consecutive', ('A', 'H', 9, 12)),
        )
        self._add_rules_from_data(m2m_field, 
            'PA Primers', data)


    def _add_dilution_factor_rules_1(self, m2m_field):
        # Distribution in English.
        # One constant value for left two thirds, and another for
        # remaining two thirds.
        data = (
            ('30', 'Consecutive', ('A', 'H', 1, 8)),
            ('', 'Consecutive', ('A', 'H', 9, 12)),
        )
        self._add_rules_from_data(m2m_field, 
            'Dilution Factor', data)

    def _add_id_primers_rules_1(self, m2m_field):
        # Distribution in English.
        # One block repeating every 4 columns, for all rows.
        primer_block = 'Eco64 Eco66, Efs03 Efs02, van30 van33, van04 van02'
        data = (
            (primer_block, 'Consecutive', ('A', 'H', 1, 12)),
        )
        self._add_rules_from_data(m2m_field, 'ID-Primers', data)

    def _add_rules_from_data(self, m2m_field, payload_type, data):
        for rule in data:
            payload, distribution_type, zone = rule
            m2m_field.add(AllocRule.make(self._tick(), 
                payload_type, payload, distribution_type, zone))

if __name__ == "__main__":
    ReferenceExperiment().create()

