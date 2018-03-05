
class NestedMixGraphNode:
    """
    The NestedMixGraphNode class can be used to construct a directed graph
    representing mixtures of mixtures..

    A node holds a mixture defined in terms of the upstream mixtures that go 
    into it.

    It also knows where it is going to be used (its targets) in terms of:
    1) Downstream mixture nodes
    2) Targetted buckets
    """

    def __init__(self):
        # Comprised of...
        self.upstream_mixture_nodes = set() 

        # Delivers to, or targets ...
        self.downstream_nodes = set()
        self.targeted_buckets = set()

    def targets_are_superset_of(self, other):
        """
        Are the places that this mixture node gets used, a superset of the 
        places that the *other* mixture node gets used?
        """
        buckets_conform = self.targeted_buckets.issuperset(
                other.targeted_buckets)
        downstream_nodes_conform = self.downstream_nodes.issuperset(
                other.downstream_nodes)
        return buckets_conform and downstream_nodes_conform

    def copy_targets_from(self, other_node):
        """
        Augment my targets with those that the other node has.
        """
        self.downstream_nodes.update(other_node.downstream_nodes)
        self.targeted_buckets.update(other_node.targeted_buckets)

    def remove_targets_that_this_has(self, other_node):
        """
        Deplete my targets by removing any that match those that the other
        node has.
        """
        self.downstream_nodes.difference_update(other_node.downstream_nodes)
        self.targeted_buckets.difference_update(other_node.targeted_buckets)

    def remove_all_targets(self):
        self.downstream_nodes = set()
        self.targeted_buckets = set()

