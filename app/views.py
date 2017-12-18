from rest_framework import viewsets

from .models import Primer
from .models import PrimerPair
from .models import Organism
from .models import Arg

from .serializers import PrimerSerializer
from .serializers import PrimerPairSerializer
from .serializers import OrganismSerializer
from .serializers import ArgSerializer


class PrimerViewSet(viewsets.ModelViewSet):
    queryset = Primer.objects.all()
    serializer_class = PrimerSerializer


class PrimerPairViewSet(viewsets.ModelViewSet):
    queryset = PrimerPair.objects.all()
    serializer_class = PrimerPairSerializer


class OrganismViewSet(viewsets.ModelViewSet):
    queryset = Organism.objects.all()
    serializer_class = OrganismSerializer


class ArgViewSet(viewsets.ModelViewSet):
    queryset = Arg.objects.all()
    serializer_class = ArgSerializer
