from hardware.qpcr import QpcrDataFile

class ExperimentResultsEntry():
    """
    Utility class to process qpcr and labchip experiment results excel file
    into the database
    """

    def __init__(self,plate_name):

        self.plate_name = plate_name



    def process_qpcr(self,file):
        """
        Utilizes existing  QpcrDataFile class to extract data from qpcr
        results excel sheet
        """

        qpcr_reader = QpcrDataFile(file_name=self.plate_name)
        qpcr_results = qpcr_reader.get_data_by_well(file)


        return qpcr_results

