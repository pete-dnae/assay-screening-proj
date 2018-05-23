from app.models.reagent_model import ReagentModel
from app.models.units_model import UnitsModel
from app.models.reagent_group_model import ReagentGroupModel
from app.models.experiment_model import ExperimentModel
from app.rules_engine.rule_script_processor import RulesScriptProcessor
from .well_constituents_maker import WellConstituentsMaker
from .well_results_summary import WellsSummaryMaker
from .labchip_results_summary import LabchipResultsSummary
from django.shortcuts import get_object_or_404

class WellResultsProcessor:

    def __init__(self,experiment_name,plate_id,wells):
        self.experiment_name = experiment_name
        self.plate_id = plate_id
        self.wells = wells
        self.allocation_results = self._fetch_allocation_results()
        self.reagent_categories = self._fetch_reagent_categories()

    def fetch_well_results(self):

        well_constituents_maker = WellConstituentsMaker(self.plate_id,
                                                        self.wells,
                                                        self.allocation_results,
                                                        self.reagent_categories)
        well_constituents = well_constituents_maker.prepare_well_constituents()
        well_summary = WellsSummaryMaker(self.experiment_name,self.plate_id,
                                         well_constituents)
        labchip_results = LabchipResultsSummary(self.experiment_name,
                                              self.plate_id,
                              self.allocation_results,
                              self.wells,well_constituents).fetch_labchip_results()
        return well_summary.prepare_vanilla_summary()



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

        return None if not alloc_table else alloc_table

    def _fetch_reagent_categories(self):
        """
        returns reagents and reagent groups from db , along with their
        category information
        """
        reagent_category = {r.name: r.category.name for r in
                            ReagentModel.objects.all()}
        reagent_category.update({r.group_name: 'group assay' for r in
                                 ReagentGroupModel.objects.all()})
        return reagent_category


    def _fetch_experiment(self):
        """"
          Fetches experiment object from db , returns http:404 if not fould
        """
        return get_object_or_404(ExperimentModel, pk=self.experiment_name)
