from hardware.labchip_peak import LabChipPeakProcessor
from app.models.qpcr_results_model import QpcrResultsModel
from app.models.reagent_model import ReagentModel
from app.models.units_model import UnitsModel
from app.models.reagent_group_model import ReagentGroupModel
from app.models.experiment_model import ExperimentModel
from app.rules_engine.rule_script_processor import RulesScriptProcessor
from django.shortcuts import get_object_or_404
import re
import math

class UnexpectedWellNameError(Exception):
    pass


class LabChipResultsProcessor:
    """
    Is responsible for orchestrating gathering of information
    about labchip wells and tagging labchip wells to the correct qpcr well
    """
    def __init__(self, plate_name, experiment_name):
        """
         Needs allocation results to trace labchip well to its parent qpcr well
         Needs  the set of 'wells' under mentioned experiment ,plate to use
         as key to pick information from labchip results
         """
        self.plate_name = plate_name
        self.experiment_name = experiment_name
        self.source_well_dict = self._fetch_source_well_dict()
        self.wells = self._fetch_wells()

    def parse_labchip_file(self, file):
        """
        Utilizes LabChipPeakProcessor to retrieve information from incoming
        file object.
        Orchestrates extraction of peak data from labchip results
        """
        labchip_reader = LabChipPeakProcessor()
        labchip_results = labchip_reader.parse_labchip_peak_data(file)
        results = []
        for well_id in self.wells:
            labchip_well = labchip_results[well_id]
            peaks = self._extract_peaks(labchip_well, well_id)
            results = results + peaks
        return results

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _extract_peaks(self, labchip_well, well_id):
        """
        orchestrates finding of source plate well for each labchip well ,
        normalizes peak data and aggregates peak results
        """
        peaks = []
        for peak_name, peak_data in labchip_well.items():

            source_well,source_plate = self._get_source_plate_well(well_id)
            qpcr_well = self._fetch_qpcr_well(source_plate, source_well)
            peaks.append({
                'experiment':self.experiment_name,
                'labchip_plate_id':self.plate_name,
                'size':self._normalize_peak_data(peak_data,'size_[bp]'),
                'concentration': self._normalize_peak_data(peak_data,'conc_('
                                                                     'ng/ul)'),
                'purity': self._normalize_peak_data(peak_data,'%_purity'),
                'peak_name': peak_name,
                'molarity': self._normalize_peak_data(peak_data,'molarity_('
                                                                'nmol/l)'),
                'labchip_well': peak_data['well_label'],
                'qpcr_well': qpcr_well.id
            })

        return peaks

    def _fetch_source_well_dict(self):
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

        return None if not alloc_table else alloc_table.source_map



    def _get_source_plate_well(self, well_position):
        """
        when called returns informations about source well and source plate
        governs conversion of well position from alphanumeric to numeric and
        vice versa
        """

        row, col = self._well_position_to_numeric(well_position)
        source_info = \
            self.source_well_dict[self.plate_name][col][row]

        source_well=\
            self._well_position_to_alpha_numeric((source_info['source_row'],
                                                  source_info['source_col']))

        source_plate = source_info['source_plate']

        return source_well,source_plate

    def _well_position_to_numeric(self, well_position):
        """
        Converts well position from alphanumeric to numeric
        """

        match = re.match(r"([A-Z])([0-9]+)", well_position)

        if not match:
            raise UnexpectedWellNameError()

        try:
            row, col = match.groups()
            numrow = ord(row) - 64
            numcol = int(col)
            return numrow, numcol
        except:
            raise UnexpectedWellNameError()

    def _well_position_to_alpha_numeric(self, well_position):
        """
        Converts well position from numeric to alphanumeric
        """

        row, col = well_position
        strcol = str(col).zfill(2)
        strrow = chr(row + 64)
        return strrow+strcol

    def _fetch_qpcr_well(self, qpcr_plate, qpcr_well):
        """"
        Fetches qpcr well object from db , returns http:404 if not fould
        """
        return get_object_or_404(QpcrResultsModel,
                                 experiment=self.experiment_name,
                                 qpcr_plate_id=qpcr_plate,
                                 qpcr_well=qpcr_well)


    def _fetch_experiment(self):
        """"
          Fetches experiment object from db , returns http:404 if not fould
        """
        return get_object_or_404(ExperimentModel, pk=self.experiment_name)

    def _fetch_wells(self):
        """
        Extracts keys from allocation_results and convert them into
        corresponding alphanumeric well_name representations
        """
        wells = []
        source_map = self.source_well_dict[self.plate_name]
        for col,rows in source_map.items():
            wells_in_row =[self._well_position_to_alpha_numeric((row,col)) for
                           row in rows.keys()]
            wells = wells+wells_in_row
        return set(wells)

    def _normalize_peak_data(self,peak_data,key):
        """
        Replaces NaN with None
        """
        if math.isnan(peak_data[key]):
            return None
        return peak_data[key]


