from rest_framework import serializers
from .models import Primer
from .models import PrimerPair
from .models import Organism
from .models import Arg
from .models import Strain
from .models import CyclingPattern


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
