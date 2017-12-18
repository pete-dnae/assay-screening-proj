from rest_framework import serializers
from .models import Primer, PrimerPair


class PrimerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Primer
        fields = ('url', 'string_code', 'direction')


class PrimerPairSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PrimerPair
        fields = ('url', 'fwd_primer', 'rev_primer', 
                'role', 'string_code')
