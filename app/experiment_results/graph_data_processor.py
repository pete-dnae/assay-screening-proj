from scipy.stats import linregress
import numpy as np
from .experiment_data_extractor import get_qpcr_results_by_well
class GraphDataProcessor:

    def __init__(self,well_constituents,qpcr_queryset):

        self.well_constituents = well_constituents
        self.qpcr_data = get_qpcr_results_by_well(qpcr_queryset)



    def prepare_amp_melt_graph(self):
        amp_data = []
        melt_data = []
        for well_id,constituents in self.well_constituents.items():
            constituents['well_id']=well_id
            amp_data.append({
                'x':self.qpcr_data[well_id]['amplification_cycle'],
                'y':self.qpcr_data[well_id]['amplification_delta_rn'],
                'meta':constituents
            })
            melt_data.append({
                'x':self.qpcr_data[well_id]['melt_temperature'],
                'y':self.qpcr_data[well_id]['melt_derivative'],
                'meta':constituents
            })
        return {'amp_data':amp_data,'melt_data':melt_data}

    def prepare_copy_count_graph(self):
        try:
            template, ct = self._get_conc_ct_values()
            eff, r2 = self.calc_eff_r2(template, ct)
            template = np.log10(template)
            x_for_fit = np.array(template, dtype=np.float32)
            a = np.vstack([x_for_fit, np.ones(len(x_for_fit))]).T
            y_for_fit = np.array(ct, dtype=np.float32)
            fit, residuals = np.linalg.lstsq(a, y_for_fit)[:2]
            slope, intercept = fit
            fitted_y = slope * x_for_fit + intercept
            return {'x1': x_for_fit.tolist(), 'y1': y_for_fit.tolist(),
                 'y2': fitted_y.tolist(), 'r2': int(r2 * 100),
                 'eff': eff}
        except:
            return {'x1': [], 'y1': [], 'y2': [], 'r2': "null",
                 'eff': "null"}


    def _get_conc_ct_values(self):
        template_conc = []
        ct_vals = []
        for well_id,constituents in self.well_constituents.items():
            if 'templates' in constituents:
                template_conc.append(self._get_concentration(constituents[
                                                                 'templates']))
                ct_vals.append(self._get_ct_value(well_id))

        return template_conc,ct_vals

    def _get_ct_value(self,well_id):
        ct =self.qpcr_data[well_id]['cycle_threshold']
        if ct is None:
            return 40
        return ct

    def _get_concentration(self,constituents):

        if len(constituents) >0 :
            return constituents[0]['concentration']
        else:
            return None

    def calc_eff_r2(self,template, ct):
        """
        Function to calculate efficiency and r2
        :param template:
        :param ct:
        :return:
        """
        log_template = np.log10(template)
        if any(np.isinf(log_template)):
            raise ValueError("Can't calculate efficeincy with 'inf' values. "
                             "Have you removed NTCs?")
        lin_fit = linregress(log_template, ct)
        eff = (10 ** (-1 / lin_fit.slope) - 1)
        r2 = lin_fit.rvalue ** 2

        return eff, r2
