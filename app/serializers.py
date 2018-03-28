from rest_framework import serializers
from pdb import set_trace as st

# Models
from .models.experiment_model import ExperimentModel
from .models.rules_script_model import RulesScriptModel
from app.models.reagent_model import ReagentModel
from app.models.reagent_category_model import ReagentCategoryModel
from app.models.reagent_group_model import ReagentGroupModel
from .models.units_model import UnitsModel

# Serialization helpers.
from app.rules_engine.rule_script_processor import RulesScriptProcessor


class ExperimentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExperimentModel
        fields = (
           'url',
           'experiment_name',
           'rules_script',
        )


class ReagentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ReagentModel
        fields = (
           'url',
           'name',
           'category',
        )

class UnitsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UnitsModel
        fields = (
           'url',
           'abbrev',
        )

class ReagentCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ReagentCategoryModel
        fields = (
           'url',
           'name',
        )

class ReagentGroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ReagentGroupModel
        fields = (
           'url',
           'name',
           'category',
           'members',
        )

    def validate(self, data):
        # Reagent categories must be the category this Group is for.
        # And reagent names must not be duplicated.
        reagents = data['members']
        group_category = data['category']
        seen = []
        for reagent in reagents:
            reagent_name = reagent.name
            if reagent_name in seen:
                raise serializers.ValidationError(
                    'Group members must not include duplicates: <%s>' %
                    reagent_name
                )
            seen.append(reagent_name)

            if reagent.category != group_category:
                raise serializers.ValidationError(
                    ('Cannot add this reagent <%s> to this group, because ' + \
                    'its category <%s> does not match the group\'s ' + \
                    'category <%s>') % (reagent.name, reagent.category.name,
                    group_category.name)
                )
        return data

    # Note *validate_xxx' naming convention triggers automatic calling.
    def foo(self, reagents):
        # Reagent categories must be the category this Group is for.
        for reagent in reagents:
            if reagent.category != self.category:
                raise serializers.ValidationError(
                    'Cannot add reagent <%s> to this group, because ' + \
                    'its category <%s> does not match the group\'s ' + \
                    'category <%s>' % (reagent.name, reagent.category,
                    self.category)
                )
        return reagents

class RulesScriptSerializer(serializers.HyperlinkedModelSerializer):

    # Camel-case to make it nice to consum as JSON.
    interpretationResults = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RulesScriptModel
        fields = (
           'url',
           'text',
           'interpretationResults',
        )

    def get_interpretationResults(self, rule_script):
        reagents = [r.name for r  in ReagentModel.objects.all()]
        units = [u.abbrev for u  in UnitsModel.objects.all()]

        interpreter = RulesScriptProcessor(
                rule_script.text, reagents, units)
        parse_error, alloc_table, line_num_mapping = \
                interpreter.parse_and_interpret()

        err = None if not parse_error else parse_error.__dict__
        table = None if not alloc_table else alloc_table.plate_info
        lnums = None if not line_num_mapping else line_num_mapping
        
        return {
            'parseError': err,
            'table': table,
            'lnums': lnums
        }
