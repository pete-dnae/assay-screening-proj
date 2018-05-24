from app.models.qpcr_results_model import QpcrResultsModel
import numpy as np
from numpy.core.umath import isnan
from clients.expt_recipes.inst_data.data_models import IdQpcrData

class WellsSummaryMaker:
    """
    Class takes in well allocation and prepares summary calculations with
    data from db
    """

    def __init__(self,experiment_id,plate_id,well_constituents):
        """
        Need experiment and plate info to extract well information from DB
        """
        self.experiment_id = experiment_id
        self.plate_id = plate_id
        self.well_constituents = well_constituents
        self.qpcr_results = self._fetch_qpcr_results()

    def prepare_nested_summary(self):
        id_qpcr_datas = {}
        max_conc_mean_tm = self._calc_max_conc_mean_tm(self.well_constituents,
                                        self.qpcr_results)
        pa_grouped = self._group_by_pa_assay(self.well_constituents)
        for pa_assay, pa_constits in pa_grouped.items():
            ntc_wells = self._get_ntc_wells(pa_constits)
            qpcr_datas = [self.qpcr_results[w] for w in ntc_wells]
            mean_ntc_ct = self.default_ct_if_nan(self.get_mean_ct(qpcr_datas))
            for well in pa_constits:
                well_data = self.qpcr_results[well]
                id_qpcr_datas[well] = IdQpcrData.create_from_db_data(well_data,
                                                 max_conc_mean_tm,
                                                 mean_ntc_ct)
        return id_qpcr_datas

    def prepare_vanilla_summary(self):
        id_qpcr_datas = {}
        max_conc_mean_tm = self._calc_max_conc_mean_tm(self.well_constituents,
                                        self.qpcr_results)
        ntc_wells = self._get_ntc_wells(self.well_constituents)
        pa_grouped = self._group_by_pa_assay(self.well_constituents)
        qpcr_datas = [self.qpcr_results[w] for w in ntc_wells]
        mean_ntc_ct = self.default_ct_if_nan(self.get_mean_ct(qpcr_datas))
        for well in self.well_constituents:
            well_data = self.qpcr_results[well]
            id_qpcr_datas[well] = IdQpcrData.create_from_db_data(well_data,
                                             max_conc_mean_tm,
                                             mean_ntc_ct)
        return id_qpcr_datas

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------




    def _fetch_qpcr_results(self):
        qpcr_result_queryset = QpcrResultsModel.objects.filter(
            experiment_id=self.experiment_id,qpcr_plate_id=self.plate_id,
            qpcr_well__in=self.well_constituents.keys())

        qpcr_results = {result['qpcr_well']:result for result in
                        qpcr_result_queryset.values()}

        return qpcr_results

    def _calc_max_conc_mean_tm(self,id_qconsts, qinst_plate):
        """
        Calculates the melting temperature ("tm") for the wells that have
        the maximum concentration of template.

        For nested experiments, these are exclusively the id only template wells.

        :param id_qconsts: a dictionary of wells containing constituents
        :param qinst_plate: qPCR instrument data
        :return:
        """
        id_template_only_wells = self._get_id_template_only_wells(id_qconsts)
        max_conc_wells = self._get_max_conc_template_from_id_wells(id_template_only_wells)
        qpcr_datas = [qinst_plate[w] for w in max_conc_wells]
        max_conc_mean_tm = self._calc_mean_tm(qpcr_datas)
        return max_conc_mean_tm

    def _get_id_template_only_wells(self,id_qconsts):
        """
        Gets a dictionary of those wells which only contain template introduced
        at the id stage.

        :param id_qconsts: a dictionary of wells containing constituents
        :return:
        """
        id_template_only_wells = {}
        for well, contents in id_qconsts.items():
            if not 'transferred_templates' in contents and \
                    'templates' in contents:
                id_template_only_wells[well] = contents
        return id_template_only_wells

    def _get_max_conc_template_from_id_wells(self,id_qconsts):
        """
        Get from the id wells, those wells that have the highest template
        concentration.

        :param id_qconsts: a dictionary of wells containing constituents
        :return:
        """
        concs = dict((w, self._get_item_attribute('templates',
                                                  'concentration',wc))
                     for w, wc in id_qconsts.items())
        max_conc_wells = {}
        concentration_values = concs.values()
        if concentration_values:
            max_conc = max(concs.values())
            for w, c in id_qconsts.items():
                if concs[w] == max_conc:
                    max_conc_wells[w] = c
        return max_conc_wells

    def _get_item_attribute(self, key, attribute,contents):
        if key in contents:
            item = contents[key]
        else:
            item = []
        attributes = tuple(i[attribute] for i in item)
        return attributes

    def _calc_mean_tm(self,qpcr_results,tm=0):
        temperatures = [result['temperatures'][tm] for result in qpcr_results]
        mean = np.mean(temperatures)
        return mean

    def _get_ntc_wells(self,well_constituents):
        """
        Gets the ntc wells from a dictionary of WellConstituents
        :param well_constituents: dictionary of WellConstituents
        :return:
        """
        return dict(
            (w, wc) for w, wc in well_constituents.items() if self._is_ntc(wc))

    def _is_ntc(self,well_constituent):
        """
        Inspects a WellConstituent instance and determines whether it's an ntc.
        :param well_constituent: a WellConstituent
        :return:
        """
        templates = [v for k, v in well_constituent.items() if 'templates' in k]
        human = [v for k, v in well_constituent.items() if 'human' in k]
        return not any(templates + human)

    def _group_by_pa_assay(self,id_qconsts):
        """
        Groups constituents by pa assay.
        :param id_qconsts: a dictionary of wells containing constituents
        :return:
        """
        wells_by_pa_assay = {}
        for w, wc in id_qconsts.items():
            pa_assay =self._get_item_attribute('transferred_assays',
                                               'reagent_name', wc)

            inner = wells_by_pa_assay.setdefault(pa_assay, {})
            inner[w] = wc
        return wells_by_pa_assay

    def get_mean_ct(self,qpcr_datas):
        """
        Gets the mean ct value from a dictionary of WellConstituents
        :param qpcr_datas: a list of qPCRInstWell instances
        :return:
        """
        cts = [qpcr['cycle_threshold'] for qpcr in qpcr_datas]
        cts = [ct for ct in cts if not ct is None]
        if cts:
            return np.mean(cts)
        else:
            return float('nan')

    def default_ct_if_nan(self,ct, default= 40):
        """
        Converts a unknown (i.e. nan) ct value to an appropriate default.
        :param ct: ct value to inspect
        :param default: default value to replace a nan
        :return:
        """
        if isnan(ct):
            return default
        else:
            return ct