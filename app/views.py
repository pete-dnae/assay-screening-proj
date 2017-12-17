from rest_framework import viewsets
from .models import Primer, PrimerPair
from .serializers import PrimerSerializer, PrimerPairSerializer


class PrimerViewSet(viewsets.ModelViewSet):
    queryset = Primer.objects.all()
    serializer_class = PrimerSerializer


class PrimerPairViewSet(viewsets.ModelViewSet):
    queryset = PrimerPair.objects.all()
    serializer_class = PrimerPairSerializer
