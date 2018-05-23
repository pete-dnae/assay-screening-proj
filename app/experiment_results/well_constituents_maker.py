from collections import OrderedDict
import re
from .labchip_results_processor import UnexpectedWellNameError


class WellConstituentsMaker:
    """
    Extracts contents related to a well from db
    """

    def __init__(self, plate_id, wells,allocation_results,
                 reagent_category):
        self.plate_id = plate_id
        self.wells = wells
        self.allocation_results = allocation_results
        self.reagent_category = reagent_category
        self.well_constituents = WellConstituents()

    def prepare_well_constituents(self):

        for well_id in self.wells:
            row, col = self._well_position_to_numeric(well_id)
            transfered_reagents = self._get_transfered_reagents(row, col)
            source_reagents = self._get_source_reagents(row, col)
            self._add__transfer_reagents_to_wells(well_id, transfered_reagents)
            self._add_reagents_to_wells(well_id, source_reagents)

        return self.well_constituents.well_info

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _add__transfer_reagents_to_wells(self, well_id, reagents):

        for reagent in reagents:
            if reagent['reagent_category'] == 'assay':
                self.well_constituents.add(well_id, 'transferred_assays',
                                           reagent)
            if reagent['reagent_category'] == 'template':
                self.well_constituents.add(well_id,
                                           'transferred_templates', reagent)
            if reagent['reagent_category'] == 'human':
                self.well_constituents.add(well_id, 'transferred_humans',
                                           reagent)

    def _add_reagents_to_wells(self, well_id, reagents):

        for reagent in reagents:
            if reagent['reagent_category'] == 'assay':
                self.well_constituents.add(well_id, 'assays', reagent)
            if reagent['reagent_category'] == 'template':
                self.well_constituents.add(well_id, 'templates', reagent)
            if reagent['reagent_category'] == 'human':
                self.well_constituents.add(well_id, 'humans', reagent)

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

    def _get_transfered_reagents(self, row, col):

        source_well = self.allocation_results.source_map[self.plate_id][
            col][row]

        if source_well:
            s_plate, s_row, s_col = self._get_source_plate_row_col(source_well)
            well_allocation = self._get_well_allocation(s_plate, s_row, s_col)
            return self._get_reagents(well_allocation)

        return []

    def _get_source_reagents(self, row, col):

        well_allocation = self._get_well_allocation(self.plate_id, row, col)
        return self._get_reagents(well_allocation)

    def _get_reagents(self, well_allocation):
        results = []
        for (reagent, conc, unit) in well_allocation:
            if reagent in self.reagent_category:
                results.append({'concentration': conc,
                                'reagent_category': self.reagent_category[
                                    reagent],
                                'reagent_name': reagent,
                                'unit': unit})
        return results

    def _get_source_plate_row_col(self, source_well):
        return source_well['source_plate'], source_well['source_row'], \
               source_well['source_col']

    def _get_well_allocation(self, plate, row, col):

        return self.allocation_results.plate_info[plate][col][row]


class WellConstituents:
    """
    A container that carries information about well constituents
    """

    def __init__(self):
        self.well_info = OrderedDict()

    def add(self, well_id, property, value):

        well_detail = self.well_info.setdefault(well_id, {})
        well_detail.setdefault(property,[]).append(value)
