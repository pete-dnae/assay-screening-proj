from collections import Counter
from pdb import set_trace as st
import sys

from .nested_mix_graph import NestedMixGraphNode


class NestedPremixer:
    """
    This class consumes the output from a FlatPremixer and works out what
    opportunities there are to build a nested graph of mixtures. Where for
    example mix P is used as a constituent in mix Q, which is used as
    a constituent in mix R. And so on.

    It captures the resultant mixture graph using NestedMixGraphNode(s).

    """

    def __init__(self, flat_premixes):
        """
        Provide the flat premixes you want to nest. Using a data structure of 
        this form. (Which is also what the FlatPremixer produces).
        Noting that this code takes no interest in the type of the things in
        the sets you provide. It performs only set operations on them.
        (
            ({'A', 'B', 'C'}, [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            ({'E', 'D'}, [0, 1, 2, 3, 4, 5]),
            ({'H', 'I', 'J'}, [0, 1, 2]),
            ({'F', 'G'}, [6, 7, 8])
        )

        Consider that:
            The ED premix is used in 012345
            The ABC premix is used in 012345678
        So there is an opportunity to premix these two to go into 012345
        Which saves 3 transfer operations.

        For this example, the full set of nested premixes this class will
        produce is:

            foo todo


        """
        self.graph_nodes = self._transform_flat_premixes_into_graph(
            flat_premixes)

    def build_nested_mixes(self):
        while True:
            succeeded = self._find_next_nesting_opportunity()
            if succeeded is False:
                return # Finished

    def dump(self):
        """
        Provides a text representation of the graph held in self.graph_nodes.
        """
        lines = []
        for node in self.graph_nodes:
            lines.append(node.dump())
        return '\n'.join(lines)
            


    #----------------------------------------------------------------------
    # Private below.
    #----------------------------------------------------------------------

    def _transform_flat_premixes_into_graph(self, flat_premixes):
        """
        Convert the flat premixes provided into the graph node format used
        here.
        """
        res = []
        for items, buckets in flat_premixes:
            node = NestedMixGraphNode()
            node.individual_items = set(items) # Take a copy
            node.targeted_buckets = set(buckets) # Take a copy
            res.append(node)
        return res

    def _find_next_nesting_opportunity(self):
        # There is a nesting opportunity, when we can find amongst our 
        # existing mixes a pair such that the buckets targeted by by one
        # is a superset of the buckets targeted by the other.
        superset, subset = self._find_nestable_pair()
        if superset is None:
            return False
        self._bring_new_node_into_being_and_do_housekeeping(superset, subset)
        return True

    def _find_nestable_pair(self):
        # Find a pair of mixture nodes such that the places targeted by
        # one are a superset of those targeted by the other.
        for super in self.graph_nodes:
            for sub in self.graph_nodes:
                if super == sub:
                    continue
                if super.targets_are_superset_of(sub):
                    return super, sub
        return None, None

    def _bring_new_node_into_being_and_do_housekeeping(
            self, superset_node, subset_node):
        """
        Consider 
            superset_node = ABC
            subset_node = ED

        We create a new mix node consuming both the paired nodes as upstream 
        nodes and adopting the targets of subset_node.
        We can then delete the subset_node as it has fallen out of use.
        And we must tell the superset_node to no longer target the targets
        which subset_node had, since these will now be covered from the new
        node.
        """
        new_node = NestedMixGraphNode()
        new_node.upstream_mixture_nodes = set((superset_node, subset_node)) 
        new_node.adopt_targets_from(subset_node)

        self.graph_nodes.append(new_node)

        superset_node.remove_targets_that_this_has(subset_node)
        if superset_node.has_no_targets():
            self.graph_nodes.remove(superset_node)
            
        self.graph_nodes.remove(subset_node)
