from hardware.qpcr import QpcrDataFile
from hardware.qpcr import get_amplification_data,get_ct,get_melt_data,get_tms
from app.models.qpcr_results_model import QpcrResultsModel
from app.models.experiment_model import ExperimentModel
from django.shortcuts import get_object_or_404

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
            temperatures = get_tms(qpcr_well)
            cycle_threshold = get_ct(qpcr_well)
            amplification_data = get_amplification_data(qpcr_well)
            melt_data = get_melt_data(qpcr_well)
            well = qpcr_well['well']
            experiment = qpcr_well['expt']
            results.append({
                'temperatures':temperatures,
                'cycle_threshold':cycle_threshold,
                'amplification_cycle':amplification_data['amplification_cycle'],
                'amplification_delta_rn':
                    amplification_data['amplification_delta_rn'],
                'melt_temperature':melt_data['melt_temperature'],
                'melt_derivative': melt_data['melt_derivative'],
                'well':well,
                'experiment':experiment,
                'plate_id':self.plate_name,
            })
        return results


    def get_experiment(self,experiment_name):
        """
        Function returns experiment object from the db , returns 404 if no
        matching objects are found
        """

        return get_object_or_404(ExperimentModel,experiment_name=experiment_name)

    def write_to_qpcr_results(self,experiment, plate_id, well, cycle_threshold,
                              temperatures,amplification_data,melt_data):

        QpcrResultsModel.make(experiment, plate_id, well, cycle_threshold,
                              temperatures,
                              amplification_data['amplification_cycle'],
                              amplification_data['amplification_delta_rn'],
                              melt_data['melt_temperature'],
                              melt_data['melt_derivative'])
