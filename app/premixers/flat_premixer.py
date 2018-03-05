from collections import Counter
from pdb import set_trace as st


class FlatPremixer:
    """
    This class came into being in the context of dispensing liquid mixtures
    into wells on a plate. When repeated patterns exist in these dispensing
    operations, it is possible to reduce the number of transfer operations 
    by pre-mixing some of the liquids in advance, and then dispensing from the
    premix into the places it is needed.

    This class tackles the first part of this problem, which is to work out
    what premixing is possible. It does NOT go on to further optimise the
    premixes by nesting them. For that see the sister NestedPremixer class
    which may be combined with this one.
    
    The code is decoupled from the original context (by design). It is able to 
    receive abstracted *mixture specifications* for *buckets*.

    In the original context, the mixtures were defined in terms of *reagent*
    name and the concentration at which each was required. This code however
    abstracts the combination of a reagent name and its concentration as an 
    *item*, and requires only that the *items* you provide are *hashable*.

    Here is an example in which the hashable items chosen are simply capital 
    letters. 

    0   ABC DE HIJ K
    1   ABC DE HIJ L
    2   ABC DE HIJ M
    3   ABC DE     N
    4   ABC DE     O
    5   ABC DE     P
    6   ABC FG     Q
    7   ABC FG     R
    8   ABC FG     S

    The premixer should find
        ({'A', 'B', 'C'}, [0, 1, 2, 3, 4, 5, 6, 7, 8])
        ({'E', 'D'}, [0, 1, 2, 3, 4, 5])
        ({'H', 'I', 'J'}, [0, 1, 2])
        ({'F', 'G'}, [6, 7, 8]),
    """

    def __init__(self, buckets):
        """
        Provide a sequence of bucket mixtures as python sets like this.
        The code takes no interest in the set-members' types.
        This example shows capital letters for ease of understanding.

        ({'A', 'B', 'C', 'F'}, {'A', 'B', 'C', 'G'}, etc ...}
        """
        self._buckets = buckets
        self._all_items = self._all_items() # Superset.

        # Accumulates results as 2-tuples: (premix_set, targeted_buckets)
        self.premixes = []

    def find_premixes(self):
        """
        Captures the recommended premixes in self.premixes.
        """
        while True:
            # Each iteration of this loop discovers and records a premix,
            # seeded with the the item that is most prolific in the buckets,
            # - then removing from the buckets, the items used in the premix 
            # each time round.
            seed_item = self._most_prolific_item() 
            if seed_item is None:
                break # Finished
            target_buckets = self._buckets_containing_item(seed_item)
            # See what other items, are *always* present alongside this
            # seed item.
            premix = self._cohabitees_of(seed_item, target_buckets)
            # Capture it.
            self.premixes.append((premix, target_buckets))
            # Housekeeping before next iteration.
            self._remove_premixed_items_from_buckets(premix, target_buckets)


    #-----------------------------------------------------------------------
    # Private below
    #-----------------------------------------------------------------------

    def _all_items(self):
        """
        The set of items across all buckets.
        """
        res = set()
        res.update(*self._buckets)
        return res

    def _most_prolific_item(self):
        """
        Evaluate the item most prevalent in the buckets, and providing its 
        frequency is greater than one, return it. Otherwise return None.
        """
        counter = Counter()
        for bucket in self._buckets:
            for item in bucket:
                counter[item] += 1
        ranked_items = counter.most_common()
        if len(ranked_items) == 0:
            return None
        item, frequency = ranked_items[0]
        return item if frequency > 1 else None

    def _cohabitees_of(self, seed_item, target_buckets):
        """
        Which other items can be found that coexist with the seed_item
        in all the same buckets as it lives in..
        """
        # Start with (a copy of) all items and then remove any item that 
        # doesn't show up in any of the target buckets.
        res = set(self._all_items)
        for i in target_buckets:
            bucket = self._buckets[i]
            res.intersection_update(bucket)
        return res

    def _buckets_containing_item(self, item):
        res = []
        for i, bucket in enumerate(self._buckets):
            if item in bucket:
                res.append(i)
        return res

    def _remove_premixed_items_from_buckets(self, premix, target_buckets):
        for i in target_buckets:
            bucket = self._buckets[i]
            bucket.difference_update(premix)
