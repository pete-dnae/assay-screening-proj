from rest_framework import viewsets


from .models import *
from .serializers import ConcentrationSerializer
from .serializers import ListExperimentSerializer
from .serializers import DetailExperimentSerializer


class MultiSerializerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A mix-in to allow a hosting serializer to offer different implementations
    for list vs. detail requests.
    Source: https://stackoverflow.com/questions/22616973/...
    django-rest-framework-use-different-serializers-in-the-same-modelviewset
    """

    def get_serializer_class(self):
        print('XXXXXX action is: %s' % self.action)
        return self.serializers.get(self.action, self.serializers['default'])


class ConcentrationViewSet(viewsets.ModelViewSet):
    queryset = Concentration.objects.all()
    serializer_class = ConcentrationSerializer

class ExperimentViewSet(MultiSerializerViewSet):
    queryset = Experiment.objects.all()

    serializers = {
        'default': None,
        'list': ListExperimentSerializer,
        'retrieve': DetailExperimentSerializer,
    }
