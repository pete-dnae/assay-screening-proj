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
from app.images.image_maker import ImageMaker

class ExperimentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExperimentModel
        fields = (
           'url',
           'experiment_name',
           'rules_script',
        )


class ReagentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReagentModel
        fields = (
           'url',
           'name',
           'category',
        )
        depth = 1


class UnitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnitsModel
        fields = (
           'url',
           'abbrev',
        )

class ReagentCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ReagentCategoryModel
        fields = (
           'name',
        )
        depth = 1

class ReagentGroupSerializer(serializers.ModelSerializer):

    reagent = ReagentSerializer
    units = UnitsSerializer
    class Meta:
        model = ReagentGroupModel
        fields = (
           'group_name',
           'reagent',
           'concentration',
           'units',
        )
        depth = 2


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
        parse_error, alloc_table,thermal_cycling_results ,line_num_mapping = \
                interpreter.parse_and_interpret()


        err = None if not parse_error else parse_error.__dict__
        table = None if not alloc_table else alloc_table.plate_info
        lnums = None if not line_num_mapping else line_num_mapping
        thermal_cycling = None if not thermal_cycling_results else \
            thermal_cycling_results.plate_info
        return {
            'parseError': err,
            'table': table,
            'lnums': lnums,
            'thermalCycling':thermal_cycling
        }

#-------------------------------------------------------------------------
# Some convenience serializers to help in particular use-cases.
#-------------------------------------------------------------------------


class MakeImageSerializer(serializers.Serializer):

    experimentImages = serializers.SerializerMethodField(read_only=True)

    def get_experimentImages(self,experiment_id):

        image_maker = ImageMaker(experiment_id)
        err,results = image_maker.make_images()

        return {
            'parseError':err,
            'results':results
        }