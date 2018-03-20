from rest_framework import serializers

from .models.experiment_model import ExperimentModel
from .models.rules_script_model import RulesScriptModel
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

    interpretation_results = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RulesScriptModel
        fields = (
           'url',
           'text',
           'interpretation_results',
        )

    def get_interpretation_results(self, rule_script):
        # todo - get these from the database when they are available
        reagents = (
            'Titanium-Taq',
            '(Eco)-ATCC-BAA-2355',
            '(Eco)-ATCC-BAA-9999')
        units = ('M/uL', 'x', 'dilution')

        interpreter = RulesScriptProcessor(
                rule_script.text, reagents, units)
        parse_error, alloc_table = interpreter.parse_and_interpret()

        return {
            'parse_error': None if not parse_error else parse_error.__dict__,
            'allocation': None if not alloc_table else alloc_table.__dict__,
        }
