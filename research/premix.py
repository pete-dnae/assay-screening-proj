class Premix:
    """
    This is an abstraction of an analysis that can be done of a 
    mandate to fill a set of *buckets* with different mixtures of *items*.

    We have a set of numbered Buckets [0,1,2..]. 
    The items that can go in them are capital letters.
    For each bucket we specify the set of letters it is to receive.

    Putting a letter into a bucket carries a cost, but we can reduce the 
    overall cost by pre-mixing sets of letters that can be deployed into 
    multiple buckets.

    This class is capable of inspecting the filling mandate and deducing
    opportunities for pre-mixing. Including some optimisation heuristics, and
    including nested pre-mixing.
    """

    def __init__(self, buckets):
        """
        Specify the buckets like this:
        ['ABC', 'ABCD', 'PQ',...]
        """
        self._buckets = buckets
        self._premixes = []
        self._assert_input_correctness()

    def find_premixes(self):
        while True:
            seed_letter = self._most_prolific_letter()
            if seed_letter is None:
                break
                fart capture target buckets here
                fart store xrefs between premixes and target bucket lists
            premix = self._expand_premix_from_seed(seed_letter)
            self._premixes.append(premix)
            self._deplete_buckets(premix, target)

   #-----------------------------------------------------------------------
   # Private below
   #-----------------------------------------------------------------------

    def _most_prolific_letter(self):
        """
        Which letter is the most prevalent across all buckets?
        """
        counter = Counter()
        for bucket in self._buckets:
            counter.update(bucket)
        chosen_letter = counter.most_common().pop()
        return chosen_letter

    def _expand_premix_from_seed(self, seed_letter):
        """
        Finds which other letters are co-located with the seed letter in all
        the same chambers as it is.
        """
        premix = {seed_letter}
        potential_letters = set(''.join(self._buckets))
        targeted_buckets = self._buckets_containing(seed_letter)
        for letter in potential_letters:
            if self._letter_is_present_in_all_of(targeted_buckets):
                premix.add(letter)
        return ''.join(list(premix).sorted())
                
    def _buckets_containing(self, letter)
        """ Which buckets contain this letter?"""
        return [bucket for bucket in self._buckets if letter in bucket]

    def _letter_is_present_in_all_of(self, letter, buckets):
        """
        Is the letter present in all these buckets?
        """
        is_in = [bucket for bucket in buckets if letter in bucket]
        return len(is_in) == len(buckets)

    def _deplete_buckets(self, premix, target_bucket_indices):
        """
        Remove all the letters in the premix from the target buckets.
        """
        for index in target_bucket_indices:
            bucket = self._buckets[index]
            retain = set(bucket) - set(premix)
            as_sorted_string = ''.join(list(retain).sort())
            self._buckets[index] = as_sorted_string

    def _assert_input_correctness(self):
        for bucket in self._buckets:
            if upper(bucket) != bucket:
                raise RuntimeError('Only upper case letters allowed in a bucket')
            if len(set(bucket)) != len(bucket):
                raise RuntimeError('No duplicate letters allowed in a bucket.')

