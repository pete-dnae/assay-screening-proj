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
    Provides an endpoint that offers Read and Update operations for a
    single instance of a RuleList instance.

    Two different Update operations are provided by PUT requests:

    To re-order the existing rules in the list, or to add or remove members,
    provide the id(s) for the replacement rules in the sequence required as 
    follows.

        { "new_rules": [1, 2, 3] }

    To cause a new placholder rule to be created, and be appended to the 
    list, provide an empty payload.

    In both cases, the **rank_for_ordering** field for each rule is adjusted 
    automatically internally.
    """
    queryset = RuleList.objects.all()
    serializer_class = RuleListSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class AllocRuleViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = AllocRule.objects.all()
    serializer_class = AllocRuleSerializer

class AllocationInstructionsViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = AllocationInstructions.objects.all()
    serializer_class = AllocationInstructionsSerializer

class PlateViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer

