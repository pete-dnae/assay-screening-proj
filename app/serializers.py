from rest_framework import serializers
from .models import Primer

class PrimerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Primer
        fields = ('url', 'code',)
