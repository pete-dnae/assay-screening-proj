
from app.models.experiment_model import *
from app.rules_engine.alloc_rule import *

class CommonModules:

    def __init__(self):
        self.reagents = ['DNA-free-Water',
                         'Titanium-PCR-Buffer',
                         'KCl',
                         'MgCl2',
                         'BSA',
                         'dNTPs',
                         'Titanium-Taq',
                         '(Eco)-ATCC-BAA-2355',
                         '(Efs-vanB)-ATCC-700802',
                         '(Kox)-ATCC-15764',
                         'Ec_uidA_6.x_Eco63_Eco60',
                         'Efs_cpn60_1.x_Efs04_Efs01',
                         'Efs_vanB_1.x_van10_van06',
                         'Efm_vanA_1.x_van05_van01',
                         'Ko_pehX_1.x_Kox05_Kox02',
                         'Kp_khe_2.x_Kpn13_Kpn01',
                         'Pm_zapA_1.x_Pmi01_Pmi05',
                         'Spo_gp_1.x_Spo09_Spo13',
                         'HgDna']
        self.units = ['mM', 'mg/ml', 'mMeach', 'copies/ul', 'uM', 'ng/ul', 'x', 'dil']

    @classmethod
    def _create_pa_cycling(cls):
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

    @classmethod
    def _create_id_cycling(cls):
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

    @classmethod
    def _create_concentrations(cls):
        for denom, numerator, pref_units in (
                (1,0.4, 'microM'),
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

    @classmethod
    def _rules_from_data(cls,data):
        rules = []
        for i,rule in enumerate(data):
            payload, zone = rule
            rules.append(AllocRule)
        return rules

