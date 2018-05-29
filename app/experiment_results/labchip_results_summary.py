from clients.expt_recipes.lost import build_labchip_datas_from_inst_data

class LabchipResultsSummary:

    def __init__(self,dilutions,labchip_results,
                 well_constituents,mapping,amplicon_lengths):

        self.well_constituents = well_constituents
        self.dilutions = dilutions
        self.labchip_results = labchip_results
        self.mapping = mapping
        self.amplicon_lengths = amplicon_lengths

    def fetch_labchip_results(self):
        return build_labchip_datas_from_inst_data(self.well_constituents,
                                           self.labchip_results,self.mapping,
                                           self.amplicon_lengths,self.dilutions)

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------


    def _get_source_plate_row_col(self,source_well):

        return source_well['source_plate'],source_well['source_row'],\
               source_well['source_col']