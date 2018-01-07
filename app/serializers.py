from rest_framework import serializers

from .models import *


class ConcentrationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Concentration
        fields = ('__all__')

class ConcreteReagentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ConcreteReagent
        fields = ('__all__')

class BufferMixSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BufferMix
        fields = ('__all__')

class MixedReagentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MixedReagent
        fields = ('__all__')

class PlaceholderReagentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PlaceholderReagent
        fields = ('__all__')

class MasterMixSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MasterMix
        fields = ('__all__')

class GeneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Gene
        fields = ('__all__')

class OrganismSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Organism
        fields = ('__all__')

class PrimerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Primer
        fields = ('__all__')

class PrimerPairSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Concentration
        fields = ('__all__')

class PrimerKitSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PrimerKit
        fields = ('__all__')

class ArgSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Arg
        fields = ('__all__')

class StrainSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Strain
        fields = ('__all__')

class StrainKitSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = StrainKit
        fields = ('__all__')

class CyclingPatternSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CyclingPattern
        fields = ('__all__')

class AllocRuleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AllocRule
        fields = ('__all__')

class AllocationInstructionsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AllocationInstructions
        fields = ('__all__')


class PlateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Plate
        fields = ('__all__')


class DetailExperimentSerializer(serializers.ModelSerializer):

    plates = PlateSerializer(many=True, read_only=True)

    class Meta:
        model = Experiment


        fields = (
           'url',
           'experiment_name',
           'designer_name',
           'plates',
        )

class ListExperimentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experiment
        fields = (
           'url',
           'experiment_name',
        )
