from hardware.labchip_peak import LabChipPeakProcessor
from app.models.qpcr_results_model import QpcrResultsModel
from app.models.reagent_model import ReagentModel
from app.models.units_model import UnitsModel
from app.models.reagent_group_model import ReagentGroupModel
from app.models.experiment_model import ExperimentModel
from app.rules_engine.rule_script_processor import RulesScriptProcessor
from django.shortcuts import get_object_or_404
import re

class UnknownWellNameError(Exception):
    pass

class LabChipResultsProcessor:

    def __init__(self,plate_name,experiment_name):

        self.plate_name = plate_name
        self.experiment_name = experiment_name
        self.allocation_results = self._fetch_allocation_results()

    def parse_labchip_file(self,file):

        labchip_reader = LabChipPeakProcessor()
        labchip_results = labchip_reader.parse_labchip_peak_data(file)
        results = []
        for well_id,labchip_well in labchip_results.items():
            peaks = self._extract_peaks(labchip_well,well_id)
            results.append(peaks)
        return results


    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _extract_peaks(self,labchip_well,well_id):

        peaks = []
        for peak_name,peak_data in labchip_well.items():
            source_info = self._get_source_plate_well(well_id)
            source_well = self._well_position_to_alpha_numeric(source_info[
                                                           'source_row'],
                                                 source_info['source_col'])
            qpcr_well = self._fetch_qpcr_well(source_info['source_plate'],
                                              source_well)
            peaks.append({
                'size':peak_data['size_[bp]'],
                'concentration':peak_data['conc_(ng/ul)'],
                'purity': peak_data['%_purity'],
                'peak_name':peak_name,
                'molarity':peak_data['molarity_(nmol/l)'],
                'labchip_well':peak_data['well_label'],
                'qpcr_well':qpcr_well
            })

        return peaks

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

        return alloc_table

    def _fetch_experiment(self):
        return get_object_or_404(ExperimentModel,pk=self.experiment_name)

    def _get_source_plate_well(self,well_position):

        row,col = self._well_position_to_numeric(well_position)
        source_info = \
            self.allocation_results.source_map[self.plate_name][col][row]

        return source_info

    def _well_position_to_numeric(self,well_position):

        match = re.match(r"([A-Z])([0-9]+)", well_position)
        if match:
            return match.groups()
        else:
            raise UnknownWellNameError()

    def _well_position_to_alpha_numeric(self,well_position):

        row,col = well_position

        return chr(row+64)+str(col)

    def _fetch_qpcr_well(self,qpcr_plate,qpcr_well):

        return get_object_or_404(experiment = self.experiment_name,
                                 qpcr_plate_id=qpcr_plate,
                                 qpcr_well=qpcr_well)