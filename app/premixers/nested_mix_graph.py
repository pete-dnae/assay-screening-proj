from pdb import set_trace as st

class NestedMixGraphNode:
    """
    The NestedMixGraphNode class can be used to construct a directed graph
    representing mixtures of mixtures..

    A node holds a mixture defined in terms of the upstream mixtures that go 
    into it, plus its own local mixture items.

    It also knows where it is going to be used (its targets) in terms of:
    1) Downstream mixture nodes
    and/or
    2) Targetted buckets
    """

    _next_name = 1

    def __init__(self, own_items, upstream_nodes):
        # Comprised of...
        self.own_items = own_items # A set
        self.upstream_mixture_nodes = upstream_nodes # A set

        # Delivers to, or targets ...
        self.downstream_nodes = set()
        self.targeted_buckets = set()

        self.name = NestedMixGraphNode._next_name
        NestedMixGraphNode._next_name += 1

    def dump(self):
        """
        Provide a text represnentation of this node.
        """
        consumes = ','.join([str(n.name) for n in self.upstream_mixture_nodes])
        downstream = ','.join([str(n.name) for n in self.downstream_nodes])
        items = self._flatten_constituent_items()
        items_str = ','.join(items)

        res = 'Node %d, consumes: %s, items: %s, downstream: %s, buckets: %s' % (
                self.name, consumes, items_str, downstream, self.targeted_buckets)
        return res


    def targets_are_superset_of(self, other_node):
        """
        Are the places that this mixture node gets used, a superset of the 
        places that the *other* mixture node gets used?
        """
        buckets_conform = self.targeted_buckets.issuperset(
                other_node.targeted_buckets)
        downstream_nodes_conform = self.downstream_nodes.issuperset(
                other_node.downstream_nodes)

        return buckets_conform and downstream_nodes_conform

    def adopt_targets_from(self, other_node):
        """
        Augment my targets with those that the other node has.
        """
        self.downstream_nodes.update(other_node.downstream_nodes)
        self.targeted_buckets.update(other_node.targeted_buckets)

    def add_downstream_node(self, node):
        self.downstream_nodes.add(node)

    def remove_targets_that_this_has(self, other_node):
        """
        Deplete my targets by removing any that match those that the other
        node has.
        """
        self.downstream_nodes.difference_update(other_node.downstream_nodes)
        self.targeted_buckets.difference_update(other_node.targeted_buckets)

    def has_no_targets(self):
        """
        Are there no targets left. (Arising from removing them.)
        """
        if len(self.downstream_nodes) != 0:
            return False
        if len(self.targeted_buckets) != 0:
            return False
        return True


    def _flatten_constituent_items(self):
        """
        Provides a set of all the items in this mix (recurses) upstream..
        """
        res = self.own_items
        for upstream in self.upstream_mixture_nodes:
            res.update(upstream._flatten_constituent_items())
        return res
