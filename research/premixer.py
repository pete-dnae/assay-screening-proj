from collections import Counter
from pdb import set_trace as st


class Premixer:
    """
    If you want to put various mixtures of *items* into some *buckets*, 
    it can be valuable to pre-mix some items in advance and then dispense 
    a share of the prepared mixture into several buckets.

    This code is able to receive mixture specifications for buckets, and deduce
    the opportunity to make pre-mixes.

    The client provides the mixture specification for each bucket (in
    sequence), by providing a set of *items* for each one. The code takes no
    interest in what the items are. It requires only that they are hashable.
    """

    def __init__(self, buckets):
        """
        Provide a sequence of bucket mixtures.
        Like this example which uses integers as items:
        ({1,2,3}, {2,3}, {2,4,5})
        """
        self._buckets = buckets
        self._all_items = self._all_items() # Superset.

        # Accumulates results as 2-tuples: (premix, targeted_buckets)
        self.premixes = []

    def find_premixes(self):
        """
        Captures the recommended premixes in self.premixes.
        """
        while True:
            seed_item = self._most_prolific_item() 
            if seed_item is None:
                break # Finished
            target_buckets = self._buckets_containing_item(seed_item)
            # See what other items, are always present alongside this
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

