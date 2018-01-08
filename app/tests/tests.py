from django.test import TestCase

from app.models.builders.make_ref_exp import ReferenceExperiment

class CreateReferenceExperiment(TestCase):

    def test_create_reference_experiment(self):
        # Just to exercise the reference experiment builder.
        experiment = ReferenceExperiment()
        experiment.create()
        self.assertTrue(True)


    def _test_create_reference_experiment(self):
        experiment = Experiment.objects.create(
            experiment_name = 'A81_E131',
            designer_name = 'NC',
            pa_mastermix = self.make_pa_mastermix(),
            id_mastermix = self.make_id_mastermix(),
            #primer_kit = self.make_primer_kit(),
            #strain_kit = self.make_strain_kit(),
            #pa_cycling = self.make_pa_cycling(),
            #id_cycling = self.make_id_cycling(),
        )
        experiment.plates.add(self.make_plate_1())
        experiment.plates.add(self.make_plate_2())
        self.assertTrue(True) # Test exists only to get model build to work.

    def make_pa_mastermix(self):
        mastermix = MasterMix.objects.create(final_volume=50)
        mastermix.concrete_reagents.add(*self.make_pa_concrete_reagents())
        mastermix.mixed_reagents.add(*self.make_pa_mixed_reagents())
        mastermix.placeholder_reagents.add(*self.make_pa_placeholder_reagents())
        return mastermix

    def make_id_mastermix(self):
        mastermix = MasterMix.objects.create(final_volume=50)
        #mastermix.concrete_reagents.add(*self.make_id_concrete_reagents())
        #mastermix.mixed_reagents.add(*self.make_id_mixed_reagents())
        #mastermix.placeholder_reagents.add(*self.make_id_placeholder_reagents())
        return mastermix

    def make_pa_concrete_reagents(self):
        reagents = []
        reagents.append(
            self._make_concrete_reagent(
                'DNA Free Water', '22884100', 0, 0, 'X')
        )
        return reagents

    def make_pa_mixed_reagents(self):
        reagents = []
        reagents.append(
            MixedReagent.objects.create(
                buffer_mix = self.make_pa_buffer_mix(),
                concentration = Concentration.objects.create(
                    stock = 3.3,
                    final = 1.0,
                    units = 'X',
                )
            )
        )
        return reagents

    def make_pa_buffer_mix(self):
        mix = BufferMix.objects.create(
            volume = 15,
            final_volume = 50,
        )
        mix.concrete_reagents.add(
            self._make_concrete_reagent(
                'Titanium PCR Buffer', '1602046A', 10, 0.13, 'X')
        )
        mix.concrete_reagents.add(
            self._make_concrete_reagent('KCl', '-', 1000, 48, 'mM')
        )
        mix.concrete_reagents.add(
            self._make_concrete_reagent('MgCl2', '449890', 25, 2.06, 'mM')
        )
        mix.concrete_reagents.add(
            self._make_concrete_reagent('BSA', '-', 20, 1, 'mg/ml')
        )
        mix.concrete_reagents.add(
            self._make_concrete_reagent('dNTPs', '-', 10, 0.2, 'mM each')
        )
        mix.concrete_reagents.add(
            self._make_concrete_reagent(
                'Titanium Taq', '1607230A', 50, 1, 'x')
        )
        return mix

    def make_pa_placeholder_reagents(self):
        reagents = []
        reagents.append(
            PlaceholderReagent.objects.create(
                type = 'Primer',
                concentration = Concentration.objects.create(
                    stock = 10,
                    final = 0.4,
                    units = 'microM each',
                ),
            )
        )
        reagents.append(
            PlaceholderReagent.objects.create(
                type = 'HgDNA',
                concentration = Concentration.objects.create(
                    stock = 120,
                    final = 60,
                    units = 'ng/ul',
                ),
            )
        )
        reagents.append(
            PlaceholderReagent.objects.create(
                type = 'Template',
                concentration = Concentration.objects.create(
                    stock = 1,
                    final = 0.1,
                    units = 'cp/ul',
                ),
            )
        )
        return reagents

    def _make_concrete_reagent(self, name, lot, stock, final, units):
        return ConcreteReagent.objects.create(
            name = name,
            lot = lot,
            concentration = \
                Concentration.objects.create(
                    stock = stock,
                    final = final,
                    units = units,
            ),
        )
