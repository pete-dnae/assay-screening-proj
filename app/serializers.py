from rest_framework import serializers

from .models import *

class ConcentrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concentration
        fields = ('url', 'stock', 'final', 'units')

class DetailExperimentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experiment
        depth = 10
        fields = (
           'url',
           'experiment_name',
           'designer_name',
           'pa_mastermix',
           'id_mastermix',
           'primer_kit',
           'strain_kit',
           'plates',
           'pa_cycling',
           'id_cycling'
        )

class ListExperimentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experiment
        fields = (
           'url',
           'experiment_name',
        )


