from collections import Counter


class Premix:
    """
    If you are going to put various mixtures of *items* into some *buckets*, 
    it can be valuable to pre-mix some items in advance and then dispense 
    a share of the prepared mixture into several buckets.

    This code is able to receive mixture specifications for buckets, and deduce
    the opportunity to make pre-mixes. Including nested pre_mixes, and a level 
    of heuristic optimisation.

    It uses buckets numbered (0,1,2...).
    The client provides the mixture specification for each bucket by providing
    a set of *items* for each one. The code takes no interest in what the 
    items are. It requires only that they are hashable.
    """

    def __init__(self, mixtures):
        """
        Example mixtures for integer items in 3 buckets:
        ({1,2,3}, {2,3}, {2,4,5})
        """
        self._mixtures = mixtures
        self._all_items = self._all_items() # A set.

    def find_premixes(self):
        while True:
            seed_item = self._most_prolific_item() 
            if seed_item is None:
                break # Finished
            target_buckets = self._buckets_containing_item(seed_item):
            # See what other items, are always present with this seed item.
            premix = self._cohabitees_of(seed_item, target_buckets)
            # Capture it.
            self._premixes.append(premix)
            # Housekeeping before next iteration.
            self._remove_premixed_items_from_buckets(premix, target_buckets)

   #-----------------------------------------------------------------------
   # Private below
   #-----------------------------------------------------------------------

    def _all_items(self):
        """
        The set of items across all buckets - in their current condition.
        """
        items = set()
        for bucket in self._buckets:
            items.union_update(bucket)
        return items

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
        item = ranked_items.pop()
        return item if counter[item] > 1 else None

    def _cohabitees_of(self, seed_item, target_buckets):
        """
        Which other items can be found that coexist with the seed_item
        in all the same buckets as it lives in..
        """
        # Start with all items and then remove any item that doesn't show up
        # in any of the target buckets.
        cohabitees = set(self._all_items) 
        for bucket in target_buckets:
            cohabitees.intersection_update(bucket)
        return cohabitees

    def _buckets_containing_item(self, item):
        buckets = [bucket for bucket in self._buckets if item in bucket]
        return buckets


    def _remove_premixed_items_from_buckets(self, premix, target_buckets):
        for bucket in target_buckets:
            bucket.intersection_update(premix)

