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

    It captures the resultant mixture graph using NestedGraphNode(s).

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
        instead of them both separately. Which saves 3 transfer operations.

        For this example, the full set of nested premixes this class will
        produce is:

            foo todo


        """
        self.graph_nodes = self._transform_flat_premixes_into_graph(
            flat_premixes)
        while True:
            succeeded = self._find_next_nesting_opportunity()
            if succeeded is False:
                return # Finished


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
        source_and_sink = self._find_source_and_sink()
        if source_and_sink is None:
            return False
        self._bring_new_node_into_being_and_do_housekeeping(source_and_sink)
        return True

    def _find_source_and_sink(self):
        # Find a source and sink node, such that the places targeted by
        # the source are supersets of those targeted by the sink.
        for source in self.graph_nodes:
            for sink in self.graph_nodes:
                if source == sink:
                    continue
                if source.targets_are_superset_of(sink):
                    return source, sink

    def _bring_new_node_into_being_and_do_housekeeping(self, source_and_sink):
        """
        Consider 
            source = ABC
            sink = ED

        We create a new mix consuming both the source and the sink mixes.
        We now instead of dispensing the sink mixture to its target places, we
        dispense the newly created mix to those places instead.
        We must also tell the source mix to stop dispensing to the places
        targeted by the sink mix.
        """
        new_node = NestedMixGraphNode()
        source, sink = source_and_sink
        new_node.upstream_mixture_nodes = set((source, sink))
        new_node.copy_targets_from(sink)
        self.graph_nodes.append(new_node)

        sink.remove_all_targets()

        source.remove_targets_that_this_has(sink)
