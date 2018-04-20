import unittest
from app.images.image_recipe import ImageRecipe
from app.model_builders.reference_data import REFERENCE_ALLOWED_NAMES
from app.model_builders.reference_data import REFERENCE_SCRIPT
from app.model_builders.reference_data import REFERENCE_UNITS
from app.rules_engine.rule_script_parser import RuleScriptParser
from app.rules_engine.rule_obj_interpreter import RulesObjInterpreter
from app.models.reagent_model import ReagentModel
from app.model_builders.make_ref_exp import ReferenceExperiment

class ImageMakerTest(unittest.TestCase):

    def setUp(self):
        ReferenceExperiment().create()

    def test_image_recipe(self):

        parser = RuleScriptParser(
            REFERENCE_ALLOWED_NAMES, REFERENCE_UNITS, REFERENCE_SCRIPT)
        parser.parse()
        machine_readable_rules = parser.rule_objects
        interpreter = RulesObjInterpreter(machine_readable_rules)
        alloc_table, thermal_cycling_results = interpreter.interpret()
        reagent_categories = \
            {r.name: r.category.name for r in ReagentModel.objects.all()}
        recipe_maker = ImageRecipe(alloc_table.plate_info['Plate1'],
                              reagent_categories)
        recipe = recipe_maker.make_image_spec()

        self.assertEquals(recipe_maker.common_reagents,
                          {('Titanium-Taq', 0.02, 'M/uL')})
        self.assertEquals(recipe[1][2],[('(Eco)-ATCC-BAA-2355', 1.16, 'x')])

        recipe_maker = ImageRecipe(alloc_table.plate_info['Plate42'],
                                   reagent_categories)
        recipe = recipe_maker.make_image_spec()

        self.assertEquals(recipe_maker.common_reagents,
                          {('Transfer Plate1:Col-1:Row-2', 20.0, 'dilution')})
        self.assertEquals(recipe[4][1], [('Ec_uidA_6.x_Eco63_Eco60', 0.4,
                                          'uM')])