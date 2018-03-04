
from app.models.experiment_model import *
from app.rules_engine.alloc_rule import *
from app.rules_engine.rule_script_parser import *
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
        self.units = ['mM', 'mg/ml', 'mMeach', 'copies', 'uM', 'ng', 'x', 'dil']

    @classmethod
    def create_pa_cycling(cls):
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
    def create_id_cycling(cls):
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


    def validate_rules(self,data):
         return RuleScriptParser(self.reagents,self.units,data)


