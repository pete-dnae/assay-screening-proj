from rest_framework import viewsets

from .serializers import *

#----------------------------------------------------------------------------
# First, a few mix-ins and utilities
#----------------------------------------------------------------------------

class MultiSerializerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A mix-in to allow a hosting serializer to offer different implementations
    for list vs. detail requests.
    Source: https://stackoverflow.com/questions/22616973/...
    django-rest-framework-use-different-serializers-in-the-same-modelviewset
    """

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])


_GET_ONLY = ['get', 'head']

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
    http_method_names = _GET_ONLY

class ConcentrationViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Concentration.objects.all()
    serializer_class = ConcentrationSerializer
    http_method_names = _GET_ONLY

class ConcreteReagentViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = ConcreteReagent.objects.all()
    serializer_class = ConcreteReagentSerializer
    http_method_names = _GET_ONLY

class BufferMixViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = BufferMix.objects.all()
    serializer_class = BufferMixSerializer
    http_method_names = _GET_ONLY

class MixedReagentViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = MixedReagent.objects.all()
    serializer_class = MixedReagentSerializer
    http_method_names = _GET_ONLY

class PlaceholderReagentViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = PlaceholderReagent.objects.all()
    serializer_class = PlaceholderReagentSerializer
    http_method_names = _GET_ONLY

class MasterMixViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = MasterMix.objects.all()
    serializer_class = MasterMixSerializer
    http_method_names = _GET_ONLY

class GeneViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer
    http_method_names = _GET_ONLY

class OrganismViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Organism.objects.all()
    serializer_class = OrganismSerializer
    http_method_names = _GET_ONLY

class PrimerViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Primer.objects.all()
    serializer_class = PrimerSerializer
    http_method_names = _GET_ONLY

class PrimerPairViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = PrimerPair.objects.all()
    serializer_class = PrimerPairSerializer
    http_method_names = _GET_ONLY

class PrimerKitViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = PrimerKit.objects.all()
    serializer_class = PrimerKitSerializer
    http_method_names = _GET_ONLY

class ArgViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Arg.objects.all()
    serializer_class = ArgSerializer
    http_method_names = _GET_ONLY

class StrainViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Strain.objects.all()
    serializer_class = StrainSerializer
    http_method_names = _GET_ONLY

class StrainKitViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = StrainKit.objects.all()
    serializer_class = StrainKitSerializer
    http_method_names = _GET_ONLY

class CyclingPatternViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = CyclingPattern.objects.all()
    serializer_class = CyclingPatternSerializer
    http_method_names = _GET_ONLY

class RuleListViewSet(viewsets.ModelViewSet):
    """
    The **PUT** option is available to change the rules inside this 
    **RuleList** or to change their order. The payload must provide a correctly
    sequenced list of the **id**s of the rules required like this:

        { "new_rules": (1, 2, 3) }

    The **rank_for_ordering** field for each rule is adjusted automatically
    internally.
    """
    queryset = RuleList.objects.all()
    serializer_class = RuleListSerializer
    http_method_names = ['get', 'put', 'head','options']

class AllocRuleViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = AllocRule.objects.all()
    serializer_class = AllocRuleSerializer
    http_method_names = _GET_ONLY

class AllocationInstructionsViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = AllocationInstructions.objects.all()
    serializer_class = AllocationInstructionsSerializer
    http_method_names = _GET_ONLY

class PlateViewSet(viewsets.ModelViewSet):
    __doc__ = _DO_NOT_USE
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer
    http_method_names = _GET_ONLY

