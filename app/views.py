from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from .view_helpers import ViewHelpers


class ExperimentViewSet(viewsets.ModelViewSet):

    queryset = ExperimentModel.objects.all()
    serializer_class =  ExperimentSerializer
    lookup_value_regex = '[a-zA-Z0-9_ ]+'

class RulesScriptViewSet(viewsets.ModelViewSet):
    queryset = RulesScriptModel.objects.all()
    serializer_class =  RulesScriptSerializer


class ReagentViewSet(viewsets.ModelViewSet):
    """
    You can specify an optional name-search criteria for the reagent, like
    this:

        /api/reagents/?name=Titanium-Taq
    """
    queryset = ReagentModel.objects.all()
    serializer_class =  ReagentSerializer
    lookup_value_regex = '[^/]+'

    def get_queryset(self):
        """
        Overridden to provide the search functionality.
        """
        name_to_search_for = self.request.query_params.get('name', None)
        if name_to_search_for:
            matching = ReagentModel.objects.filter(name=name_to_search_for)
            return matching
        return ReagentModel.objects.all()

class UnitViewSet(viewsets.ModelViewSet):
    queryset = UnitsModel.objects.all()
    serializer_class = UnitsSerializer
    lookup_value_regex = '.+'


class ReagentCategoryViewSet(viewsets.ModelViewSet):
    queryset = ReagentCategoryModel.objects.all()
    serializer_class = ReagentCategorySerializer


class ReagentGroupViewSet(viewsets.ModelViewSet):
    queryset = ReagentGroupModel.objects.all()
    serializer_class = ReagentGroupSerializer

    def get_queryset(self):
        """
        Overridden to provide the search functionality.
        """
        name_to_search_for = self.request.query_params.get('name', None)
        if name_to_search_for:
            matching = ReagentGroupModel.objects.filter(group_name=name_to_search_for)
            return matching
        return ReagentGroupModel.objects.all()

#-------------------------------------------------------------------------
# Some convenience (non-model) views.
#-------------------------------------------------------------------------

class AllowedNamesView(APIView):

    def get(self, request, format=None):
        return Response(ViewHelpers.all_allowed_names())


class ExperimentImagesView(APIView):
    """
    Creates MakeImageSerializer with the experiment id which then provides the
    resultant JSON data structure in data property of the object instance
    """

    def get(self,request,experiment_id):
        results = MakeImageSerializer(experiment_id).data
        return Response(results)

class ReagentGroupListView(APIView):
    """
    Returns list of unique reagent group names in db
    """

    def get(self,request):
        results = ReagentGroupModel.objects.values('group_name').distinct()
        return Response(results)