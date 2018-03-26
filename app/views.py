from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *

class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = ExperimentModel.objects.all()
    serializer_class =  ExperimentSerializer

class RulesScriptViewSet(viewsets.ModelViewSet):
    queryset = RulesScriptModel.objects.all()
    serializer_class =  RulesScriptSerializer

class ReagentViewSet(viewsets.ModelViewSet):
    queryset = ReagentModel.objects.all()
    serializer_class =  ReagentSerializer

class UnitViewSet(viewsets.ModelViewSet):
    queryset = UnitsModel.objects.all()
    serializer_class =  UnitsSerializer

class ReagentCategoryViewSet(viewsets.ModelViewSet):
    queryset = ReagentCategoryModel.objects.all()
    serializer_class =  ReagentCategorySerializer

class ReagentGroupViewSet(viewsets.ModelViewSet):
    queryset = ReagentGroupModel.objects.all()
    serializer_class =  ReagentGroupSerializer
