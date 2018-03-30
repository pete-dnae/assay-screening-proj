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
           'group_name',
           'reagent',
           'concentration',
           'units',
        )

    def validate(self, data):
        # Reagent names must not already exist in the group.
        group_name = data['group_name']
        reagent_name = data['reagent'].name
        existing_member_names = [group.reagent.name for group in \
            ReagentGroupModel.objects.filter(group_name=group_name)]
        if reagent_name in existing_member_names:
            raise serializers.ValidationError(
                ('Cannot add <%s> to group <%s> because it ' + \
                'already contains it.') % (reagent_name, group_name)
            )
        return data


class RulesScriptSerializer(serializers.HyperlinkedModelSerializer):

    # Camel-case to make it nice to consume as JSON.
    interpretationResults = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RulesScriptModel
        fields = (
           'url',
           'text',
           'interpretationResults',
        )

    def get_interpretationResults(self, rule_script):
        reagent_names = [r.name for r in ReagentModel.objects.all()]
        group_names = set([g.group_name for g in \
                ReagentGroupModel.objects.all()])
        allowed_names = reagent_names + list(group_names)
        units = [u.abbrev for u in UnitsModel.objects.all()]

        interpreter = RulesScriptProcessor(
                rule_script.text, allowed_names, units)
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

#-------------------------------------------------------------------------
# Some convenience serializers to help in particular use-cases.
#-------------------------------------------------------------------------
