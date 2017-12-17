from rest_framework import serializers
from .models import Primer, PrimerPair


class PrimerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Primer
        fields = ('url', 'code', 'direction')


class PrimerPairSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PrimerPair
        fields = ('id', 'url', 'fwd', 'rev', 'role')
