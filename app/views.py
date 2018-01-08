from rest_framework import viewsets

from .serializers import *
from .models import *


"""
from .models import Concentration
from .models import ConcreteReagent
from .models import BufferMix
from .models import MixedReagent
from .models import PlaceholderReagent
from .models import MasterMix
from .models import Gene
from .models import Organism
from .models import Primer
from .models import PrimerPair
from .models import PrimerKit
from .models import Arg
from .models import Strain
from .models import StrainKit
from .models import CyclingPattern
from .models import AllocRule
from .models import AllocationInstructions
from .models import Plate
from .models import Experiment
"""


class MultiSerializerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A mix-in to allow a hosting serializer to offer different implementations
    for list vs. detail requests.
    Source: https://stackoverflow.com/questions/22616973/...
    django-rest-framework-use-different-serializers-in-the-same-modelviewset
    """

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])


class ExperimentViewSet(MultiSerializerViewSet):
    queryset = Experiment.objects.all()

    serializers = {
        'default': None,
        'list': ListExperimentSerializer,
        'retrieve': DetailExperimentSerializer,
    }

class ConcentrationViewSet(viewsets.ModelViewSet):
    queryset = Concentration.objects.all()
    serializer_class = ConcentrationSerializer

class ConcreteReagentViewSet(viewsets.ModelViewSet):
    queryset = ConcreteReagent.objects.all()
    serializer_class = ConcreteReagentSerializer

class BufferMixViewSet(viewsets.ModelViewSet):
    queryset = BufferMix.objects.all()
    serializer_class = BufferMixSerializer

class MixedReagentViewSet(viewsets.ModelViewSet):
    queryset = MixedReagent.objects.all()
    serializer_class = MixedReagentSerializer

class PlaceholderReagentViewSet(viewsets.ModelViewSet):
    queryset = PlaceholderReagent.objects.all()
    serializer_class = PlaceholderReagentSerializer

class MasterMixViewSet(viewsets.ModelViewSet):
    queryset = MasterMix.objects.all()
    serializer_class = MasterMixSerializer

class GeneViewSet(viewsets.ModelViewSet):
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer

class OrganismViewSet(viewsets.ModelViewSet):
    queryset = Organism.objects.all()
    serializer_class = OrganismSerializer

class PrimerViewSet(viewsets.ModelViewSet):
    queryset = Primer.objects.all()
    serializer_class = PrimerSerializer

class PrimerPairViewSet(viewsets.ModelViewSet):
    queryset = PrimerPair.objects.all()
    serializer_class = PrimerPairSerializer

class PrimerKitViewSet(viewsets.ModelViewSet):
    queryset = PrimerKit.objects.all()
    serializer_class = PrimerKitSerializer

class ArgViewSet(viewsets.ModelViewSet):
    queryset = Arg.objects.all()
    serializer_class = ArgSerializer

class StrainViewSet(viewsets.ModelViewSet):
    queryset = Strain.objects.all()
    serializer_class = StrainSerializer

class StrainKitViewSet(viewsets.ModelViewSet):
    queryset = StrainKit.objects.all()
    serializer_class = StrainKitSerializer

class CyclingPatternViewSet(viewsets.ModelViewSet):
    queryset = CyclingPattern.objects.all()
    serializer_class = CyclingPatternSerializer

class AllocRuleViewSet(viewsets.ModelViewSet):
    queryset = AllocRule.objects.all()
    serializer_class = AllocRuleSerializer

class AllocationInstructionsViewSet(viewsets.ModelViewSet):
    queryset = AllocationInstructions.objects.all()
    serializer_class = AllocationInstructionsSerializer

class PlateViewSet(viewsets.ModelViewSet):
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer
