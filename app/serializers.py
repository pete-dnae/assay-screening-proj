from rest_framework import serializers

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
from .models import RowPattern
from .models import AllocationInstructions
from .models import Plate
from .models import Experiment




class ConcentrationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Concentration
        fields = ('url', 'id', 'stock', 'final', 'units')


class ConcreteReagentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ConcreteReagent
        fields = ('url', 'id', 'stock', 'final', 'units', 'concentration')


class PrimerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Primer
        fields = ('url', 'string_code', 'direction')


class PrimerPairSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PrimerPair
        fields = ('url', 'fwd_primer', 'rev_primer', 
                'role', 'string_code')


class OrganismSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Organism
        fields = ('url', 'abbreviation', 'full_name')


class ArgSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Arg
        fields = ('url', 'name')



class StrainSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Strain
        fields = ('url', 'name', 'organism', 'arg', 'genome_size')


class CyclingPatternSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CyclingPattern
        fields = ('url', 'pattern_name', 'activation_time', 'activation_temp',
            'num_cycles', 'denature_temp', 'denature_time', 'anneal_temp', 
            'anneal_time', 'extend_temp', 'extend_time')
