import unittest
from app.rules_engine.rule_script_parser import *
class PremixerTest(unittest.TestCase):


    def setUp(self):
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
        self.units = ['mM', 'mg/ml', 'mMeach', 'copies/ul', 'uM', 'ng/ul', 'x']

        self.script = "V 1 \n" \
                      "P 1 \n" \
                      "A DNA-free-Water            1-12    A-H 3.35 x \n" \
                      "A Titanium-PCR-Buffer       1-12    A-H 0.63 x \n" \
                      "A KCl                       1-12    A-H 2.40 mM \n" \
                      "A MgCl2                     1-12    A-H 4.13 mM \n" \
                      "A BSA                       1-12    A-H 2.5 mg/ml \n" \
                      "A dNTPs                     1-12    A-H 1.00 mMeach \n" \
                      "A Titanium-Taq              1-12    A-H 1.00 x \n" \
                      "A (Eco)-ATCC-BAA-2355       1,5,9   A-B   0 copies/ul \n" \
                      "A (Eco)-ATCC-BAA-2355       1,5     C-H   5 copies/ul \n" \
                      "A (Eco)-ATCC-BAA-2355       9       C-D   50 copies/ul \n" \
                      "A (Eco)-ATCC-BAA-2355       9       E-F   500 copies/ul \n" \
                      "A (Eco)-ATCC-BAA-2355       9       G-H   5000 copies/ul \n" \
                      "A (Efs-vanB)-ATCC-700802    2,6,10  A-B   0 copies/ul \n" \
                      "A (Efs-vanB)-ATCC-700802    2,6     C-H   5 copies/ul \n" \
                      "A (Efs-vanB)-ATCC-700802    10      C-D   50 copies/ul \n" \
                      "A (Efs-vanB)-ATCC-700802    10      E-F   500 copies/ul \n" \
                      "A (Efs-vanB)-ATCC-700802    10      G-H   5000 copies/ul \n" \
                      "A (Efs-vanB)-ATCC-700802    3,7,11  A-B   0 copies/ul \n" \
                      "A (Efs-vanB)-ATCC-700802    3,7     C-H   5 copies/ul \n" \
                      "A (Efs-vanB)-ATCC-700802    11      C-D   50 copies/ul \n" \
                      "A (Efs-vanB)-ATCC-700802    11      E-F   500 copies/ul \n" \
                      "A (Efs-vanB)-ATCC-700802    11      G-H   5000 copies/ul \n" \
                      "A (Kox)-ATCC-15764          4,8,12  A-B   0 copies/ul \n" \
                      "A (Kox)-ATCC-15764          4,8     C-H   5 copies/ul \n" \
                      "A (Kox)-ATCC-15764          12      C-D   50 copies/ul \n" \
                      "A (Kox)-ATCC-15764          12      E-F   500 copies/ul \n" \
                      "A (Kox)-ATCC-15764          12      G-H   5000 copies/ul \n" \
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
                      "A HgDna                     1-12    A-E   0 ng/ul \n" \
                      "A HgDna                     9-12    F-H   0 ng/ul \n" \
                      "A HgDna                     1-8     E-H   3000 ng/ul"

    def test_simple_case(self):
        script_parser = RuleScriptParser(self.reagents,self.units,self.script)
        rules = script_parser.parse()

