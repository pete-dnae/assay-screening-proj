from rest_framework import viewsets

from .serializers import *

#----------------------------------------------------------------------------
# First, a few mix-ins and utilities
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Now, the usual View definitions.
#----------------------------------------------------------------------------

class ExperimentViewSet(viewsets.ModelViewSet):
    """
    POST:
    Creates a completely new Experiment by cloning the one you specify in the
    payload like this:

        { "experiment_to_copy": 1 }

    """
    queryset = ExperimentModel.objects.all()
    serializer_class =  ExperimentSerializer

class RulesScriptViewSet(viewsets.ModelViewSet):
    queryset = RulesScriptModel.objects.all()
    serializer_class =  RulesScriptSerializer
