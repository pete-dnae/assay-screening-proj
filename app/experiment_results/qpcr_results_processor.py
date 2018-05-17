from hardware.qpcr import QpcrDataFile
from hardware.qpcr import get_amplification_data,get_ct,get_melt_data,get_tms


class QpcrResultsProcessor():
    """
    Utility class to extract useful information to store from excel
    files
    containing QPCR experiment results
    """

    def __init__(self,plate_name):

        self.plate_name = plate_name



    def parse_qpcr_file(self,file):
        """
        Utilizes existing  QpcrDataFile class to extract data from qpcr
        results excel file
        """

        qpcr_reader = QpcrDataFile(file_name=self.plate_name)
        qpcr_results = qpcr_reader.get_data_by_well(file)
        results =[]

        for well_id,qpcr_well in qpcr_results.items():
            refined_well = self._refine_qpcr_well(qpcr_well)
            results.append(refined_well)
        return results

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _refine_qpcr_well(self,qpcr_well):
        """
        Extracts well properties that are part of QpcrResultsModel

        """
        temperatures = get_tms(qpcr_well)
        cycle_threshold = get_ct(qpcr_well)
        amplification_data = get_amplification_data(qpcr_well)
        melt_data = get_melt_data(qpcr_well)
        well = qpcr_well['well']
        experiment = qpcr_well['expt']

        return {
                'temperatures':temperatures,
                'cycle_threshold':cycle_threshold,
                'amplification_cycle':amplification_data['amplification_cycle'],
                'amplification_delta_rn':
                    amplification_data['amplification_delta_rn'],
                'melt_temperature':melt_data['melt_temperature'],
                'melt_derivative': melt_data['melt_derivative'],
                'qpcr_well':well,
                'experiment':experiment,
                'qpcr_plate_id':self.plate_name,
            }