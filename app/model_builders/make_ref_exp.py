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
        self._create_constant_like_things()
        self._create_concrete_reagents()
        self._create_organisms_and_strains()
        self._create_genes_and_primers()

    def _create_constant_like_things(self):
        Allocatable.objects.create(type='Unspecified')
        Allocatable.objects.create(type='Dilution-Factor')
        Allocatable.objects.create(type='HgDNA')
        Allocatable.objects.create(type='PA-Primers')
        Allocatable.objects.create(type='ID-Primers')
        Allocatable.objects.create(type='Strain')
        Allocatable.objects.create(type='Strain-Count')

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
        self._add_rules_from_data(m2m_field, self._alloc_type('Strain'), data)

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
            self._alloc_type('Strain-Count'), data)


    def _add_hg_dna_rules_1(self, m2m_field):
        # Distribution in English.
        # Blanket fill with 0 everywhere.
        # Then 3000 in a bottom left block.
        data = (
            ('0', 'Consecutive', ('A', 'H', 1, 12)),
            ('5000', 'Consecutive', ('F', 'H', 1, 8)),
        )
        self._add_rules_from_data(m2m_field, self._alloc_type('HgDNA'), data)

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
            self._alloc_type('PA-Primers'), data)


    def _add_dilution_factor_rules_1(self, m2m_field):
        # Distribution in English.
        # One constant value for left two thirds, and another for
        # remaining two thirds.
        data = (
            ('30', 'Consecutive', ('A', 'H', 1, 8)),
            ('', 'Consecutive', ('A', 'H', 9, 12)),
        )
        self._add_rules_from_data(m2m_field, 
            self._alloc_type('Dilution-Factor'), data)

    def _add_id_primers_rules_1(self, m2m_field):
        # Distribution in English.
        # One block repeating every 4 columns, for all rows.
        primer_block = 'Eco64 Eco66, Efs03 Efs02, van30 van33, van04 van02'
        data = (
            (primer_block, 'Consecutive', ('A', 'H', 1, 12)),
        )
        self._add_rules_from_data(m2m_field,
            self._alloc_type('ID-Primers'), data)

    def _add_rules_from_data(self, m2m_field, payload_type, data):
        for rule in data:
            payload, distribution_type, zone = rule
            m2m_field.add(self._create_alloc_rule(self._tick(), 
                payload_type, payload, distribution_type, zone))

    def _create_alloc_rule(self, rank_for_ordering, payload_type, payload_csv,
            pattern, zone):
        sr, er, sc, ec = zone
        return AllocRule.objects.create(
            rank_for_ordering=rank_for_ordering,
            payload_type=payload_type,
            payload_csv=payload_csv,
            pattern=pattern,
            start_row_letter=sr,
            end_row_letter=er,
            start_column=sc,
            end_column=ec,
        )

    def _alloc_type(self, type_string):
        """
        Provide the database object corresponding to the allocatable type
        with the given type string.
        """
        return Allocatable.objects.get(type=type_string)


if __name__ == "__main__":
    ReferenceExperiment().create()

