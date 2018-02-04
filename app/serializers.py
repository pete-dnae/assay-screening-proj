from rest_framework import serializers


from .models.experiment_model import *
from .models.reagent_models import *
from .models.primer_models import *
from .models.strain_models import *
from .models.plate_models import *

from app.rules_engine.alloc_rule_interpreter import AllocRuleInterpreter

# It would be nicer to group these class definitions in a way that aided
# comprehension but we cannot, because they comprise nested definitions, and
# thus must appear in dependency order for the module to load.

class AllocRuleSerializer(serializers.HyperlinkedModelSerializer):

    display_string = serializers.CharField(read_only=True)
    id=serializers.ReadOnlyField()

    class Meta:
        model = AllocRule
        exclude = ('rank_for_ordering', )


class RuleListSerializer(serializers.HyperlinkedModelSerializer):
    """
    A serializer that supports the retrieval or wholesale replacement of a 
    RuleList instance. 
    """

    # The fields for the read and write cases are completely
    # different, and mutually exclusive...
    
    # When reading, we send back all the rules' details using a nested
    # serializer for the m2m field.
    rules = AllocRuleSerializer(many=True, read_only=True)

    # To replace the list of rules wholesale, we expect to receive a list of 
    # the id(s) for the replacement rules.
    new_rules = serializers.ListField(
        child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = RuleList
        fields = ('__all__')

    def update(self, instance, validated_data):
        self._replace_rules(instance, validated_data['new_rules'])
        return instance

    def _replace_rules(self, instance, new_rule_ids):
        # Retreive all the AllocRules called for by the incoming request,
        # and set their ranking order field in accordance with their 
        # position in the list.
        new_rules = []
        for id in new_rule_ids:
            try:
                rule = AllocRule.objects.get(pk=id)
                new_rules.append(rule)
            except AllocRule.DoesNotExist:
                raise serializers.ValidationError(
                    'There is no AllocRule with this id: %d' % id)
        RuleList.apply_ranking_order_to_rule_objs(new_rules)

        # Delete the AllocRules that will fall out of use once the list
        # replacement is done.
        incumbent_ids = set([rule.id for rule in instance.rules.all()])
        to_delete_ids = incumbent_ids - set(new_rule_ids)
        AllocRule.objects.filter(pk__in=to_delete_ids).delete()

        # Repopulate the m2m field to swap out the incumbent rules with the
        # new.
        instance.rules.clear()
        instance.rules.add(*new_rules)
        instance.save()


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


class ConcentrationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Concentration
        fields = ('__all__')


class PrimerPairSerializer(serializers.HyperlinkedModelSerializer):

    display_name = serializers.SerializerMethodField()

    class Meta:
        model = PrimerPair
        fields = ('display_name',)

    def get_display_name(self, instance):
        return instance.display_name()


class PrimerKitSerializer(serializers.HyperlinkedModelSerializer):

    fwd_concentration = ConcentrationSerializer(read_only=True)
    rev_concentration = ConcentrationSerializer(read_only=True)
    id_primers = PrimerPairSerializer(many=True, read_only=True)
    pa_primers = PrimerPairSerializer(many=True, read_only=True)

    class Meta:
        model = PrimerKit
        fields = ('__all__')


class StrainSerializer(serializers.HyperlinkedModelSerializer):

    display_name = serializers.SerializerMethodField()

    def get_display_name(self, instance):
        return instance.display_name()

    class Meta:
        model = Strain
        fields = ('display_name',)


class StrainKitSerializer(serializers.HyperlinkedModelSerializer):

    strains = StrainSerializer(many=True, read_only=True)

    class Meta:
        model = StrainKit
        fields = (('url', 'strains'))


class DetailExperimentSerializer(serializers.ModelSerializer):

    plates = PlateSerializer(many=True, read_only=True)
    primer_kit = PrimerKitSerializer(read_only=True)
    strain_kit = StrainKitSerializer(read_only=True)

    class Meta:
        model = Experiment

        fields = (
           'url',
           'experiment_name',
           'designer_name',
           'plates',
           'primer_kit',
           'strain_kit',
        )


class ListExperimentSerializer(serializers.ModelSerializer):

    experiment_to_copy = serializers.IntegerField(write_only=True)

    class Meta:
        model = Experiment
        fields = (
           'url',
           'experiment_name',
           'designer_name',
           'experiment_to_copy',
        )

    def create(self, validated_data):
        # Create an experiment as a clone of the one requested.
        id = validated_data['experiment_to_copy']
        try:
            experiment_to_copy = Experiment.objects.get(id=id)
        except Experiment.DoesNotExist: 
            raise serializers.ValidationError(
                    'There is no Experiment with this id: %d' % id)

        exp = Experiment.clone(experiment_to_copy)
        return exp


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

class ArgSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Arg
        fields = ('__all__')


class CyclingPatternSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CyclingPattern
        fields = ('__all__')
