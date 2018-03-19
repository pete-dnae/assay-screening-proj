from rest_framework import serializers


from .models.experiment_model import ExperimentModel
from .models.rules_script_model import RulesScriptModel

from app.rules_engine.rule_script_parser import ParseError


# It would be nicer to group these class definitions in a way that aided
# comprehension but we cannot, because they comprise nested definitions, and
# thus must appear in dependency order for the module to load.

class ExperimentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExperimentModel
        fields = (
           'url',
           'experiment_name',
           'rules_script',
        )

class RulesScriptSerializer(serializers.HyperlinkedModelSerializer):

    error = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RulesScriptModel
        fields = (
           'url',
           'text',
           'error',
        )

    def get_error(self, rule_script):
        return ParseError('contents of parse error', 999).__dict__
