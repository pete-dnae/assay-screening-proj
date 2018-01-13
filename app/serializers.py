from rest_framework import serializers


from .models.experiment_model import *
from .models.reagent_models import *
from .models.primer_models import *
from .models.strain_models import *
from .models.plate_models import *
from app.rules_engine.alloc_rule_interpreter import AllocRuleInterpreter

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

    display_string = serializers.CharField(read_only=True)

    class Meta:
        model = AllocRule
        fields = ('__all__')


class RuleListSerializer(serializers.HyperlinkedModelSerializer):

    # The fields for the read and write cases are completely
    # different, and mutually exclusive...
    
    # When reading, we send back all the rules' details using a nested
    # serializer for the m2m field.
    rules = AllocRuleSerializer(many=True, read_only=True)

    # When writing we expect to receive a list of integers, that we will
    # treat as the ids for existing rules that should form the replacement
    # list contents. Hence the need for a custom validator.
    new_rules = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    

    class Meta:
        model = RuleList
        fields = ('__all__')

    def update(self, instance, validated_data):
        # Retreive all the AllocRules called for by the incoming request,
        # thus implicitly validating this input.
        new_ids = validated_data['new_rules'] # Retain requested sequence.
        new_objs = [AllocRule.objects.get(pk=id) for id in new_ids]

        # Set the *rank_for_ordering* field on each AllocRule in the new list 
        # to model the right sequence, as defined by the new_id list.
        for idx, rule in enumerate(new_objs):
            rule.rank_for_ordering = idx
            rule.save()

        # Delete the AllocRules that will fall out of use once the list
        # replacement is done.
        incumbent_ids = set([rule.id for rule in instance.rules.all()])
        to_delete_ids = incumbent_ids - set(new_ids)
        AllocRule.objects.filter(pk__in=to_delete_ids).delete()

        # Repopulate the m2m field to swap out the incumbent rules with the
        # new.
        instance.rules.clear()
        instance.rules.add(new_objs)

        instance.save()
        return instance


class AllocationInstructionsSerializer(serializers.HyperlinkedModelSerializer):

    rule_list = RuleListSerializer()
    allocation_results = serializers.SerializerMethodField('alloc_results')

    class Meta:
        model = AllocationInstructions
        fields = (
            'url',
            'rule_list',
            'suppressed_columns',
            'allocation_results'
        )

    def alloc_results(self, allocation_instructions):
        # The rules are ordered by definition in rank order.
        rules = allocation_instructions.rule_list.rules.all()
        rule_interpreter = AllocRuleInterpreter(rules)
        tabulated_result = rule_interpreter.interpret()
        return tabulated_result


class PlateSerializer(serializers.HyperlinkedModelSerializer):

    allocation_instructions = AllocationInstructionsSerializer(read_only=True)

    class Meta:
        model = Plate
        fields = ('url', 'name', 'allocation_instructions')


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
