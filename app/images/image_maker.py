from app.models.experiment_model import ExperimentModel
from app.models.reagent_model import ReagentModel
from app.models.units_model import UnitsModel
from app.models.reagent_group_model import ReagentGroupModel,\
    ReagentGroupDetailsModel
from app.rules_engine.rule_script_processor import RulesScriptProcessor
from app.images.image_recipe import ImageRecipe
from django.shortcuts import get_object_or_404

class ImageMaker:
    """
    Class is responsible for generating images for a given experiment

    The class returns a json serializable dictionary with plate name as
    keys and visualization information in dictionaries as values.
    It also returns a error string along with results, defaults to none if no
    errors present

    Class orchestrates the fetching of relevant experiment , then its rule
    script then use rule script processor to get hold of allocation results .
    For each plate it then instantiates an ImageRecipe to get image
    specification which is then stored in the return object keyed by
    plate name.

    """
    """
    Update 23/07/2018
        Additional function _fetch_reagent_categories to inject reagent 
        category information into image recipe
    """
    def __init__(self, experiment_name):
        """
        Provide experiment name to instantiate the class , allocation_results
        are generated after parsing experiments rule_script.
        """
        self.experiment_name = experiment_name
        self.allocation_results = self._fetch_allocation_results()
        self.images = {}

    def make_images(self):
        """
        Iterates through plates in allocation results and co-ordinates
        creation of image-spec using ImageRecipe
        """
        if self.allocation_results:
            reagent_categories = self._fetch_reagent_categories()
            for plate_name, plate_info in self.allocation_results.items():
                recipe_maker = ImageRecipe(plate_info,reagent_categories)
                image_spec = recipe_maker.make_image_spec()
                self.images[plate_name] = image_spec
            return None, self.images
        else:
            err = 'There are no allocation results for the script'
            return err, None
    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _fetch_allocation_results(self):
        """
          Fetches experiment ,prepares allowed reagents and units.
          Co-ordinates interpretation of ruleScript to produce allocation
          results.
          Returns None if errors are present
        """
        experiment = self._fetch_experiment()
        reagent_names = [r.name for r in ReagentModel.objects.all()]
        group_names = set([g.group_name for g in \
                           ReagentGroupModel.objects.all()])
        allowed_names = reagent_names + list(group_names)
        units = [u.abbrev for u in UnitsModel.objects.all()]

        interpreter = RulesScriptProcessor(
           experiment.rules_script.text, allowed_names, units)
        parse_error, alloc_table, thermal_cycling_results, line_num_mapping = \
            interpreter.parse_and_interpret()

        return None if not alloc_table else alloc_table.plate_info

    def _fetch_experiment(self):
        return get_object_or_404(ExperimentModel,pk=self.experiment_name)

    def _fetch_reagent_categories(self):
        """
        returns reagents and reagent groups from db , along with their
        category information
        """
        reagent_category = {r.name: r.category.name for r in
                            ReagentModel.objects.all()}

        for r in ReagentGroupModel.objects.all():
            group_element = ReagentGroupDetailsModel.objects.filter(
                reagent_group=r.group_name).first()
            reagent_category[r.group_name] = group_element.reagent.category.name

        return reagent_category
