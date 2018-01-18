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
    id = serializers.ReadOnlyField()

    class Meta:
        model = AllocRule
        fields = ('__all__')


class RuleListSerializer(serializers.HyperlinkedModelSerializer):
    """
    A serializer that supports the retrieval and update of a RuleList 
    instance. Two update operations are supported - the first replaces the
    AllocRules in the many to many field completely, whereas the other
    appends a rule of the clients choice onto the end of it.
    """

    # The fields for the read and write cases are completely
    # different, and mutually exclusive...
    
    # When reading, we send back all the rules' details using a nested
    # serializer for the m2m field.
    rules = AllocRuleSerializer(many=True, read_only=True)

    # To replace the list of rules wholesale, receive a list of the id(s)
    # for the replacement rules.
    new_rules = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False)

    # To append a new rule to the list, provide the id of an existing one
    # that can be copied to become the new one.
    rule_to_copy = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = RuleList
        fields = ('__all__')
        # Because we use one of these objects as a hyperlinkedmodelserializer
        # field from the AllocationInstructionSerializer, we are obliged to
        # specify the view name it should use as the reverse-lookup key when
        # synthesizing the url to show as the link.
        extra_kwargs = { 'url': {'view_name': 'viewlist-detail'} }

    def update(self, instance, validated_data):
        _NEW_RULES = 'new_rules'
        _RULE_TO_COPY = 'rule_to_copy'
        if _NEW_RULES in validated_data:
            self._replace_rules(instance, validated_data[_NEW_RULES])
        elif _RULE_TO_COPY in validated_data:
            self._append_rule(instance, validated_data[_RULE_TO_COPY])
        else:
            raise serializers.ValidationError(
                "Must have either %s or %s key in payload." %
                (_NEW_RULES, _RULE_TO_COPY))
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

    def _append_rule(self, instance, rule_id_to_copy):
        incumbent_ids = [rule.id for rule in instance.rules.all()]
        new_rule = RuleList.make_copy_of(rule_id_to_copy)
        instance.rules.add(new_rule)
        ids_to_sequence = incumbent_ids + [new_rule.id,]
        RuleList.apply_ranking_order_to_rule_ids(ids_to_sequence)
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
