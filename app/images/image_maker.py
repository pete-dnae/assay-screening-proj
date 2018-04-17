from app.models.experiment_model import ExperimentModel
from app.models.reagent_model import ReagentModel
from app.models.units_model import UnitsModel
from app.models.reagent_group_model import ReagentGroupModel
from app.rules_engine.rule_script_processor import RulesScriptProcessor
from app.images.image_recipe import ImageRecipe
from app.images.image_renderer import ImageRenderer


class ImageMaker:
    """
    Orchestrates  first the fetching of relevant experiment , then its rule script
    then user rule script processor to get hold of allocation results .

    For each plate it then instantiates an ImageRecipe and pass page the images made
    to serializer
    """

    def __init__(self, experiment_id):
        self.experiment_id = experiment_id
        self.experiment = self._fetch_experiment()
        self.allocation_results = self._fetch_allocation_results()
        self.reagent_category = self._fetch_reagent_category_dict()

    def prepare_images(self):
        for plate_name, plate_info in self.allocation_results.items():
            recipe_maker = ImageRecipe(plate_info, self.reagent_category, [])
            image_spec = recipe_maker.prepare_image_spec()
            ImageRenderer(image_spec).prepare_html_viz()

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _fetch_allocation_results(self):
        reagent_names = [r.name for r in ReagentModel.objects.all()]
        group_names = set([g.group_name for g in \
                           ReagentGroupModel.objects.all()])
        allowed_names = reagent_names + list(group_names)
        units = [u.abbrev for u in UnitsModel.objects.all()]

        interpreter = RulesScriptProcessor(
            self.experiment.rules_script.text, allowed_names, units)
        parse_error, alloc_table, thermal_cycling_results, line_num_mapping = \
            interpreter.parse_and_interpret()

        return None if not alloc_table else alloc_table.plate_info

    def _fetch_experiment(self):
        return ExperimentModel.objects.get(pk=self.experiment_id)

    @staticmethod
    def _fetch_reagent_category_dict():
        return {r.name: r.category.name for r in ReagentModel.objects.all()}
