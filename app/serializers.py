from rest_framework import serializers
from pdb import set_trace as st

# Models
from .models.experiment_model import ExperimentModel
from .models.rules_script_model import RulesScriptModel
from app.models.reagent_model import ReagentModel
from app.models.reagent_category_model import ReagentCategoryModel
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
