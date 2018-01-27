from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics

from .serializers import *

#----------------------------------------------------------------------------
# First, a few mix-ins and utilities
#----------------------------------------------------------------------------

class MultiSerializerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A mix-in to allow a hosting serializer to offer different implementations
    for list vs. detail requests.
    Source: https://stackoverflow.com/questions/22616973/...
    django-rest-framework-use-different-serializers-in-the-same-ReadOnlyModelViewSet
    """

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])


_DO_NOT_USE = '# DO NOT CONSUME THIS API (YET) - IT IS FOR INFO ONLY'

#----------------------------------------------------------------------------
# Now, the usual View definitions.
#----------------------------------------------------------------------------

class ExperimentViewSet(MultiSerializerViewSet):
    queryset = Experiment.objects.all()

    serializers = {
        'default': None,
        'list': ListExperimentSerializer,
        'retrieve': DetailExperimentSerializer,
    }

class ConcentrationViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Concentration.objects.all()
    serializer_class = ConcentrationSerializer

class ConcreteReagentViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = ConcreteReagent.objects.all()
    serializer_class = ConcreteReagentSerializer

class BufferMixViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = BufferMix.objects.all()
    serializer_class = BufferMixSerializer

class MixedReagentViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = MixedReagent.objects.all()
    serializer_class = MixedReagentSerializer

class PlaceholderReagentViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = PlaceholderReagent.objects.all()
    serializer_class = PlaceholderReagentSerializer

class MasterMixViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = MasterMix.objects.all()
    serializer_class = MasterMixSerializer

class GeneViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer

class OrganismViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Organism.objects.all()
    serializer_class = OrganismSerializer

class PrimerViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Primer.objects.all()
    serializer_class = PrimerSerializer

class PrimerPairViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = PrimerPair.objects.all()
    serializer_class = PrimerPairSerializer

class PrimerKitViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = PrimerKit.objects.all()
    serializer_class = PrimerKitSerializer

class ArgViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Arg.objects.all()
    serializer_class = ArgSerializer

class StrainViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Strain.objects.all()
    serializer_class = StrainSerializer

class StrainKitViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = StrainKit.objects.all()
    serializer_class = StrainKitSerializer

class CyclingPatternViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = CyclingPattern.objects.all()
    serializer_class = CyclingPatternSerializer


class RuleListDetail(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        generics.GenericAPIView):
    """
    A Rule List is an ordered sequence of Alloc Rule(s), i.e. 
    allocation rules.

    You can replace the incumbent sequence with a new one using a *PUT* request,
    for which the payload should be a list of the replacement Alloc Rule
    *id(s)*. Like this:

        { "new_rules": [1, 2, 3] }

    """
    queryset = RuleList.objects.all()
    serializer_class = RuleListSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class AllocRuleViewSet(viewsets.ModelViewSet):
    """
    *Alloc Rule* is short for "Allocation Rule".

    It encapsulates a recipe for repeating patterns of things like *primers,
    strains, HgDNA* (and similar) to a rectangular region of an imaginary table.
    The type of thing being repeated is specified in the *payload_type* field,
    and must be one of the following:
        
        Dilution Factor
        HgDNA
        PA Primers
        ID Primers
        Strain
        Strain Count

    The list of strings to be repeated are specified (concatenated) in the
    *payload_csv* field. 
    
    The target region of the table is defined in terms of row and column
    ranges.  Two allocation recipes are provided to replicate and multiply the
    items column-wise. Consider the payload_csv being
    
        'A,B,C'
    
    The first recipe *Consecutive*, will do this until it runs out of columns:
    
        A B C A B C A B... 

    The second recipe with fill the available column range *In Blocks* of
    equal size like this.

        AAAA.. BBBB.. CCCC.. 

    PATCH:
    Partial / selective update of a stored rule. Typically the user edited a
    rule.

    POST:
    Creates a completely new rule.
    Typically the user wants to add a new rule to a Rule List, so the client 
    is creating a new instance in readiness to do that.
    All fields are required except for id, url and display_string..
    """
    queryset = AllocRule.objects.all()
    serializer_class = AllocRuleSerializer
    http_method_names = ['get', 'patch', 'post', 'head', 'options']

class AllocationInstructionsViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = AllocationInstructions.objects.all()
    serializer_class = AllocationInstructionsSerializer

class PlateViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer
