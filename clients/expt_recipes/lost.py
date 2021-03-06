from clients.expt_recipes.inst_data.data_models import LabChipData,\
    LabChipMetaData
# todo: decouple id_qconsts from this function
def build_labchip_datas_from_inst_data(id_qconsts, linst_plate, ql_mapping,
                                       assays, dilutions):
    """
    Build a dictionary of LabchipData instances keyed on their parent
    qPCR well.

    :param id_qconsts: a dictionary of id well constituents
    :param linst_plate: a dictionary of labchip instrument data
    :param ql_mapping: a dictionary that maps between qPCR and labchip wells
    :param assays: a dictionary that maps between an assay and it's expected
    amplicon length
    :param dilutions: a dictionary of labchip wells and their dilution factors
    :return:
    """
    lc_datas = {}
    for idw, constits in id_qconsts.items():
        # If a Labchip was run, populate an instance
        if idw in ql_mapping and ql_mapping[idw]:
            lcw = ql_mapping[idw]
            ass =[assay['reagent_name'] for assay in constits['assays']]
            lc_datas[idw] = \
                LabChipData.create_from_inst_data(linst_plate[lcw],
                                                  [assays[a] for a in ass],
                                                  dilutions[lcw])
        else:
            # Or create an empty instance
            lc_datas[idw] = LabChipData()
    return lc_datas

def build_labchip_datas_from_db_data(id_qconsts, ldb_plate, ql_mapping,
                                       assays, dilutions):
    """
    Build a dictionary of LabchipData instances keyed on their parent
    qPCR well.

    :param id_qconsts: a dictionary of id well constituents
    :param ldb_plate: a dictionary of labchip instrument data
    :param ql_mapping: a dictionary that maps between qPCR and labchip wells
    :param assays: a dictionary that maps between an assay and it's expected
    amplicon length
    :param dilutions: a dictionary of labchip wells and their dilution factors
    :return:
    """
    lc_datas = {}
    for idw, constits in id_qconsts.items():
        # If a Labchip was run, populate an instance
        if idw in ql_mapping and ql_mapping[idw]:
            lcw = ql_mapping[idw]
            ass =[assay['reagent_name'] for assay in constits['assays']]
            labchip_data = LabChipData.create_from_db_data(ldb_plate[lcw],
                                                  [assays[a] for a in ass],
                                                  dilutions[lcw])
            labchip_meta = LabChipMetaData.create_from_db_data(ldb_plate[lcw])
            lc_datas[idw] = {**labchip_data,**labchip_meta}
        else:
            # Or create an empty instance
            lc_datas[idw] = LabChipData()
    return lc_datas



def is_ntc(well_constituent):
    """
    Inspects a WellConstituent instance and determines whether it's an ntc.
    :param well_constituent: a WellConstituent
    :return:
    """
    templates = [v for k, v in well_constituent.items() if 'templates' in k]
    human = [v for k, v in well_constituent.items() if 'human' in k]
    return not any(templates + human)


def get_ntc_wells(well_constituents):
    """
    Gets the ntc wells from a dictionary of WellConstituents
    :param well_constituents: dictionary of WellConstituents
    :return:
    """
    return dict((w, wc) for w, wc in well_constituents.items() if is_ntc(wc))