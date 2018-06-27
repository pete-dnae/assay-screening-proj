import json
from rest_framework import serializers
# Models
from .models.experiment_model import ExperimentModel
from .models.rules_script_model import RulesScriptModel
from app.models.reagent_model import ReagentModel
from app.models.reagent_category_model import ReagentCategoryModel
from app.models.reagent_group_model import ReagentGroupModel
from app.models.reagent_group_model import ReagentGroupDetailsModel
from app.models.qpcr_results_model import QpcrResultsModel
from app.models.labchip_results_model import LabChipResultsModel
from .models.units_model import UnitsModel
from app.models.reagent_well_lookup_model import ReagentWellLookupModel
from app.models.reagent_group_well_lookup_model import ReagentGroupWellLookupModel
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
            'experiment_type'
        )


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


class ReagentSerializer(serializers.ModelSerializer):
    category = ReagentCategorySerializer

    class Meta:
        model = ReagentModel
        fields = (
            'name',
            'category',
            'opaque_json_payload'
        )

    def validate_opaque_json_payload(self, opaque_json_payload):
        # opaque payload should be json.
        if opaque_json_payload:
            try:
                json_object = json.loads(opaque_json_payload)
            except ValueError:
                raise serializers.ValidationError('Opaque payload is not a '
                                                  'valid json')
        return opaque_json_payload


class ReagentGroupDetailsSerializer(serializers.ModelSerializer):
    reagent = ReagentSerializer
    units = UnitsSerializer

    class Meta:
        model = ReagentGroupDetailsModel
        fields = (
            'reagent',
            'concentration',
            'units',
        )


class ReagentGroupSerializer(serializers.ModelSerializer):

    details = ReagentGroupDetailsSerializer(many=True)

    class Meta:
        model = ReagentGroupModel
        fields = ('group_name','details')

    def create(self, validated_data):
        group_details = validated_data.pop('details')
        reagent_group = ReagentGroupModel.objects.create(**validated_data)
        for group_detail in group_details:
            ReagentGroupDetailsModel.objects.create(reagent_group=reagent_group,
                                                    **group_detail)
        return reagent_group




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
        parse_error, alloc_table, thermal_cycling_results, line_num_mapping = \
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
            'thermalCycling': thermal_cycling
        }


class QpcrResultsSerializer(serializers.ModelSerializer):

    experiment = ExperimentSerializer
    class Meta:
        model = QpcrResultsModel
        fields = (
            'experiment',
            'qpcr_plate_id',
            'qpcr_well',
            'cycle_threshold',
            'temperatures',
            'amplification_cycle',
            'amplification_delta_rn',
            'melt_temperature',
            'melt_derivative',
            'exclude_well',
            'comment'
        )

class LabChipResultsSerializer(serializers.ModelSerializer):

    qpcr_well = QpcrResultsSerializer
    class Meta:
        model = LabChipResultsModel
        fields = (
            'labchip_well',
            'peak_name',
            'size',
            'concentration',
            'purity',
            'qpcr_well',
            'experiment',
            'labchip_plate_id',
            'exclude_well',
            'comment'
        )

class ReagentWellLookupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReagentWellLookupModel
        fields = (
            'well',
            'reagent',
            'transfer'
        )

class ReagentGroupWellLookupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReagentGroupWellLookupModel
        fields = (
            'well',
            'reagent_group',
            'transfer'
        )


# -------------------------------------------------------------------------
# Some convenience serializers to help in particular use-cases.
# -------------------------------------------------------------------------


class MakeImageSerializer(serializers.Serializer):
    experimentImages = serializers.SerializerMethodField(read_only=True)

    def get_experimentImages(self, experiment_id):
        image_maker = ImageMaker(experiment_id)
        err, results = image_maker.make_images()

        return {
            'parseError': err,
            'results': results
        }
