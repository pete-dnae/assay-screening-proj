from app.models.labchip_results_model import LabChipResultsModel
from app.models.qpcr_results_model import QpcrResultsModel
from .labchip_results_processor import UnexpectedWellNameError
from clients.expt_recipes.lost import build_labchip_datas_from_inst_data
import re

class LabchipResultsSummary:

    def __init__(self,experiment_id,plate_id,allocation_results,qpcr_wells,
                 well_constituents):

        self.experiment_id = experiment_id
        self.plate_id = plate_id
        self.well_constituents = well_constituents
        self.allocation_results = allocation_results
        self.qpcr_wells = qpcr_wells
        self.labchip_plate = '20180103_A'
        self.assays = {'Ab_pgaD_x.10_Aba38_Aba42': 225,
                        'Ca_rpb7_x.1_Cal04_Cal03': 215,
                        'Cg_rps0_x.1_Cgl03_Cgl04': 217,
                        'Ec_uidA_x.2_Eco64_Eco66': 240}

    def fetch_labchip_results(self):
        mapping,labchip_results = self._fetch_labchip_data()
        dilutions = self._fetch_dilutions()
        return build_labchip_datas_from_inst_data(self.well_constituents,
                                           labchip_results,mapping,
                                           self.assays,dilutions)
    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _fetch_labchip_data(self):
        qpcr_result_queryset = QpcrResultsModel.objects.filter(
            experiment_id=self.experiment_id,qpcr_plate_id=self.plate_id,
            qpcr_well__in=self.qpcr_wells)
        qpcr_well_id_dict = {record['id']:record['qpcr_well'] for record in
                             qpcr_result_queryset.values('id','qpcr_well')}

        labchip_results_queryset = LabChipResultsModel.objects.filter(
            qpcr_well__in = qpcr_well_id_dict.keys()
        )
        labchip_qpcr_well_lookup = {peak['labchip_well']:qpcr_well_id_dict[
            peak['qpcr_well_id']]for peak in labchip_results_queryset.values(
            'qpcr_well_id','labchip_well')}
        qpcr_labchip_well_lookup = {v:k for (k,v) in
                                    labchip_qpcr_well_lookup.items()}
        labchip_results = {}
        for labchip in labchip_results_queryset.values():
            labchip_results.setdefault(labchip['labchip_well'],
                                               {})[labchip['peak_name']]={
                '%_purity':labchip['purity'],
                'conc_(ng/ul)':labchip['concentration'],
                'molarity_(nmol/l)':labchip['molarity'],
                'size_[bp]': labchip['size'],

            }
        return labchip_results,qpcr_labchip_well_lookup


    def _fetch_dilutions(self):
        dilution_dict = {}
        for col,rows in self.allocation_results.source_map[
            self.labchip_plate].items():
            for row,source_info in rows.items():
                well_id = self._well_position_to_alpha_numeric((col,row))
                s_plate,s_row,s_col = self._get_source_plate_row_col(
                    source_info)
                well_allocation = self.allocation_results.plate_info[
                    s_plate][s_col][s_row]
                dilutions = [conc for (reagent,conc,unit) in well_allocation if
                             unit == 'dilution']
                if len(dilutions)>0:
                    dilution_dict[well_id] = dilutions[0]
        return dilution_dict
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
        return strrow + strcol

    def _get_source_plate_row_col(self,source_well):

        return source_well['source_plate'],source_well['source_row'],\
               source_well['source_col']