from rest_framework import viewsets
from .models import Primer
from .serializers import PrimerSerializer

class PrimerViewSet(viewsets.ModelViewSet):
    queryset = Primer.objects.all()
    serializer_class = PrimerSerializer
