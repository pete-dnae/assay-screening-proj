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
        print('XXXXX at start dump is \n%s' % self.dump())
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
            upstream_nodes = set()
            node = NestedMixGraphNode(items, upstream_nodes)
            node.targeted_buckets = set(buckets) # Take a copy
            res.append(node)
        return res

    def _find_next_nesting_opportunity(self):
        # There is a nesting opportunity, when we can find amongst our 
        # existing mixes a pair such that the targets of one
        # is a superset of the targets of the other.
        superset, subset = self._find_nestable_pair()
        if superset is None:
            return False
        self._bring_new_node_into_being_and_do_housekeeping(superset, subset)
        return True

    def _find_nestable_pair(self):
        # Find a pair of mixture nodes that still have live targets, and 
        # such that the places targeted by one are a superset of those 
        # targeted by the other.
        for super in self.graph_nodes:
            for sub in self.graph_nodes:
                if super == sub: # Can't pair self with self.
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

        We must tell both the superset node and the subset node that they
        should no longer target the targets that the subset node had because
        these will now be covered by the new node.

        And we must tell the superset_node about its new downstream mix.
        """
        print('XXXX going to combine %d and %d for latters targets' % (superset_node.name, subset_node.name))
        own_items = set()
        upstream = set((superset_node, subset_node)) 
        new_node = NestedMixGraphNode(own_items, upstream)
        new_node.adopt_targets_from(subset_node)

        self.graph_nodes.append(new_node)

        superset_node.remove_targets_that_this_has(subset_node)
        subset_node.remove_targets_that_this_has(subset_node)

        superset_node.add_downstream_node(new_node)
        subset_node.add_downstream_node(new_node)
            
        print('XXXXX new node added, now dump is \n%s' % self.dump())
        st()
