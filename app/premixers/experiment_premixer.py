from collections import Counter,defaultdict
from pdb import set_trace as st
from .premixer import Premixer
from collections import Counter
from app.reagents.reagent_models import Reagent
class ExperimentPremixer:

    def __init__(self,allocResults):

        self._allocation_results=allocResults
        self._buckets = self._flatten_results(self._allocation_results)
        self.premixer_results = None
        self.buffer_mix = None
        self.buffer_mix_volume = 15
        self.buffer_mix_final_volume = 50
        self.master_mix_volume = 50
        self.buffer_mix_table = None
        self.stock_dict =  {
            'Titanium-PCR-Buffer':10,
            'KCl':1000,
            'MgCl2':25,
            'BSA':20,
            'dNTPs':10,
            'Titanium-Taq':50,
            '(Eco)-ATCC-BAA-2355': 1,
            '(Efs-vanB)-ATCC-700802': 1,
            '(Kox)-ATCC-15764': 1,
            'Ec_uidA_6.x_Eco63_Eco60': 10,
            'Efs_cpn60_1.x_Efs04_Efs01': 10,
            'Efs_vanB_1.x_van10_van06': 10,
            'Efm_vanA_1.x_van05_van01': 10,
            'Ko_pehX_1.x_Kox05_Kox02': 10,
            'Kp_khe_2.x_Kpn13_Kpn01': 10,
            'Pm_zapA_1.x_Pmi01_Pmi05': 10,
            'Spo_gp_1.x_Spo09_Spo13': 10,
            'HgDna': 120
        }
    def extract_premixes(self):
        """
        Function flattens the allocation results object to a array of sets containing hash value of reagents used per
        cell in each  set
        Premixer object is then created with the flat array and *find_premixes()* function is called to find premixes for
        the input array.
        """
        # We can use a generic premixer utility
        premixer = Premixer(self._buckets)
        premixer.find_premix_opportunities()
        premixer.find_buffermix()
        #reagent sets as premix
        self.premixer_results = premixer.premixes
        # reagent sets as buffermix
        self.buffer_mix = premixer.buffer_mix
        #dictionary with buffermix/premix calculations done
        self.buffer_mix_table = self._prepare_buffer_mix(self.stock_dict)
        self.master_mix_table = self.__prepare_master_mix(self.stock_dict)
        return #undecided


    # -----------------------------------------------------------------------
    # Private below
    # -----------------------------------------------------------------------

    def _flatten_results(self,allocation_results):
        """
        Function flatens the allocation results dictionary into a single array
        array contains a set per each column ,each set then contains the hash
        value of the reagents present in them
        """
        flat_array=[]
        for result_table in allocation_results:
            for rowkey, row in result_table.rows.items():
                for colkey,column in row.items():
                    flat_array.append(set(column))
        return flat_array

    def _prepare_buffer_mix(self,stock_dict):
        """
        Math for the identified buffer mix goes here , expects stock values to be provided
        """
        #Have a seperate class to hold the results ?
        buffer_calc_dict = {}
        remaining_vol = self.buffer_mix_volume
        for reagent in self.buffer_mix:
            final_conc = reagent.concentration.numerical_value
            stock_conc = stock_dict[reagent.name]
            final_vol = (final_conc/stock_conc)*self.buffer_mix_final_volume
            buffer_calc_dict[reagent]={
                'Stock_conc':stock_conc,
                'final_conc':final_conc,
                'final_vol':final_vol,
                'units':reagent.concentration.preferred_units
            }
            remaining_vol-=final_vol
        buffer_calc_dict[Reagent('DNA-free-water',0.00,'x')] = {
                'Stock_conc':'',
                'final_conc':'',
                'final_vol':remaining_vol,
                'units':'x'
            }
        return buffer_calc_dict

    def __prepare_master_mix(self,stock_dict):
        """
       Math for the identified buffer mix goes here , expects stock values to be provided
       """
        master_calc_dict = defaultdict(dict)
        for i,master_mix in enumerate(self.premixer_results):
            #seperate fn to handle removal of buffermix stuff from mastermix?
            remaining_volume = self.master_mix_volume - sum([x['final_vol'] for i, x in self.buffer_mix_table.items()])
            master_calc_dict[i].update(self.buffer_mix_table)
            for reagent in master_mix:
                if reagent in self.buffer_mix_table:
                    continue
                else:
                    final_conc = self._get_master_mix_reagent_conc(reagent)
                    stock_conc = stock_dict[reagent.name]
                    final_vol = (final_conc / stock_conc) * self.buffer_mix_final_volume
                    master_calc_dict[i][reagent]={'Stock_conc':stock_conc,'final_conc':final_conc,
                                              'final_vol':final_vol,'units':reagent.concentration.preferred_units}
                    remaining_volume -= final_vol

            master_calc_dict[i][Reagent('DNA-free-water', 0.00, 'x')] = {
                'Stock_conc': '',
                'final_conc': '',
                'final_vol': remaining_volume,
                'units': 'x'
            }
        return master_calc_dict

    def _check_pure_solvent(self,reagent):
        """
        Function returns true if mentioned unit represents only solvent weight
        """
        if reagent.concentration.preferred_units in ('copies','ng'):
            return True


    def _solvent_conc(self,reagent,volune):
        """
        calculate amount of solution to procure to get mentioned solvent weight
        """
        return reagent.concentration.numerical_value/volune

    def _get_master_mix_reagent_conc(self,reagent):
        if self._check_pure_solvent(reagent):
            return self._solvent_conc(reagent,self.master_mix_volume)
        else:
            return reagent.concentration.numerical_value

    def _deduct_buffer_mix_calc(self):
        buffer_mix_vol = sum([x['final_vol'] for i, x in self.buffer_mix_table.items()])
        remaining_volume = self.master_mix_volume - buffer_mix_vol
        return remaining_volume,self.buffer_mix_table