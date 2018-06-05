from app.models import *
from app.management.commands.bulk_load_reagents import Loader as ReagentLoader
from app.management.commands.bulk_load_groups import Loader as GroupLoader

import os
from app.experiment_results.qpcr_results_loader import load_qpcr_results
from app.experiment_results.labchip_results_loader import load_labchip_results
nested_rule_script \
    = """V ver-1
# PA plates
P A81_E214_1_PA
A Titanium-PCR-Buffer      1-8    A-H     0.13 x
A KCl                      1-8    A-H     48   mM
A MgCl2                    1-8    A-H     2.06 mM
A BSA                      1-8    A-H     1    mg/ml
A dNTPs                    1-8    A-H     0.2  mM
A Titanium-Taq             1-8    A-H     1    x
A poolE1                   1-4    A-H     1    x
A Ca_rpb7_2.x_Cal05_Cal01  5      A-H     0.4  uM
A Cg_rps0_1.x_Cgl02_Cgl06  6      A-H     0.4  uM
A Ab_pgaD_2.x_Aba26_Aba28  7      A-H     0.4  uM
A Ec_uidA_6.x_Eco63_Eco60  8      A-H     0.4  uM
A C.albicans_10231         1,5    C-H     5    cp
A C.glabrata_15545         2,6    C-H     5    cp
A A.baumannii_1605         3,7    C-H     5    cp
A E.coli-CTXM9_2355        4,8    C-H     5    cp
A HgDNA_Promega287320      1-8    B,F,G,H 3000 ng
C 120@95                                  1    x
C 10@95,20@62,45@72                       20   x
#
# ID plates
P A81_E214_1_ID
A KCl                      1-12   A-H     48   mM
A MgCl2                    1-12   A-H     2.06 mM
A BSA                      1-12   A-H     1    mg/ml
A SYBRgreen                1-12   A-H     0.32 x
A Triton                   1-12   A-H     0.04 %
A dNTPs                    1-12   A-H     0.2  mM
A KOH                      1-12   A-H     1.0  mM
A Titanium-Taq             1-12   A-H     1.3  x
A Ca_rpb7_x.1_Cal04_Cal03  1,5,9  A-H     0.4  uM
A Cg_rps0_x.1_Cgl03_Cgl04  2,6,10 A-H     0.4  uM
A Ab_pgaD_x.10_Aba38_Aba42 3,7,11 A-H     0.4  uM
A Ec_uidA_x.2_Eco64_Eco66  4,8,12 A-H     0.4  uM
A C.albicans_10231         9      C-D     50   cp
A C.albicans_10231         9      E-F     500  cp
A C.albicans_10231         9      G-H     5000 cp
A C.glabrata_15545         10     C-D     50   cp
A C.glabrata_15545         10     E-F     500  cp
A C.glabrata_15545         10     G-H     5000 cp
A A.baumannii_1605         11     C-D     50   cp
A A.baumannii_1605         11     E-F     500  cp
A A.baumannii_1605         11     G-H     5000 cp
A E.coli-CTXM9_2355        12     C-D     50   cp
A E.coli-CTXM9_2355        12     E-F     500  cp
A E.coli-CTXM9_2355        12     G-H     5000 cp
T A81_E214_1_PA 1-8 A-H    1-8    A-H     30   dilution
C 120@95                                  1    x
C 20@95,25@62                             40   x
#
# Labchip plates
P 20180103_A
T A81_E214_1_ID 1 A-H      1      A-H     10   dilution
T A81_E214_1_ID 2 A-H      1      I-P     10   dilution
T A81_E214_1_ID 3 A-H      2      A-H     10   dilution
T A81_E214_1_ID 4 A-H      2      I-P     10   dilution
T A81_E214_1_ID 5 A-H      3      A-H     10   dilution
T A81_E214_1_ID 6 A-H      3      I-P     10   dilution
T A81_E214_1_ID 7 A-H      4      A-H     10   dilution
T A81_E214_1_ID 8 A-H      4      I-P     10   dilution
T A81_E214_1_ID 9 A-H      5      A-H     10   dilution
T A81_E214_1_ID 10 A-H     5      I-P     10   dilution
T A81_E214_1_ID 11 A-H     6      A-H     10   dilution
T A81_E214_1_ID 12 A-H     6      I-P     10   dilution
"""

def make_test_experiment():
    root = os.path.abspath(os.getcwd())
    _load_units()
    load_reagents(root)
    load_groups(root)
    load_experiment()
    load_qpcr_data(root)
    load_labchip_data(root)

def _load_units():
    units = ["M/uL", "x", "uM", "dilution", "mM", "nM", "mg/ml", "ug/ml",
             "ng/ul", "%", "cp/ul", "cp", "ng"]
    for unit in units:
        UnitsModel.make(unit)

def load_reagents(root):
    with open(root + r'/app/model_builders/customers-seed-data/reagents'
                     r'.csv') \
            as file:
        ReagentLoader.load(file)

def load_groups(root):
    with open(
            root + r'/app/model_builders/customers-seed-data/pools.csv') as \
            file:
        GroupLoader.load(file)

def load_experiment():
    rule_script = RulesScriptModel.make(nested_rule_script)
    ExperimentModel.make('A81_E214', 'nested', rule_script)

def load_qpcr_data(root):
    with open(root + r'/hardware/tests/data/A81_E214_1_ID.xls', 'rb') as \
            file:
        load_qpcr_results('A81_E214', 'A81_E214_1_ID', file)

def load_labchip_data(root):
    with open(root + r'/hardware/tests/data/2018-01-03_11-08'
                     r'-50_A81_20180103_A_PeakTable.csv', 'rb') as \
            file:
        load_labchip_results('A81_E214', '20180103_A', file)
