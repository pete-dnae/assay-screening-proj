from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .serializers import *
from .view_helpers import ViewHelpers
from rest_framework import status
from rest_framework.exceptions import ValidationError, ParseError
from django.db.models.deletion import ProtectedError

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

    def destroy(self, request, *args, **kwargs):
        """
        Overridden to handle issues with foreign key constraints
        """

        try:
            pk = kwargs['pk']
            ReagentModel.objects.filter(pk=pk).delete()
        except ProtectedError:
            raise ValidationError('The Reagent is a part of reagent group '
                                  'hence it cannot be deleted')

        return Response(status=status.HTTP_204_NO_CONTENT)


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
            matching = ReagentGroupModel.objects.filter\
                (group_name=name_to_search_for)
            return matching
        return ReagentGroupModel.objects.all()

    def create(self, request, *args, **kwargs):
        """
        create a list of reagent group instances if a list is provided or a
        single instance otherwise

        deletes existing instances under the same reagent group name
        """

        data = request.data
        if isinstance(data,list):
            group_name = data[0]['group_name']
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            group_name = data['group_name']
            serializer = self.get_serializer(data=request.data)

        with transaction.atomic():
            ReagentGroupModel.objects.filter(group_name=group_name).delete()
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        return Response(serializer.data)


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
        return Response(ViewHelpers.group_names())

    def delete(self, request):
        try:
            group_name = request.data['group_name']
            with transaction.atomic():
                ReagentGroupModel.objects.filter(group_name=group_name).delete()
        except KeyError:
            raise ValidationError('Invalid request;Please mention a group name')

        return Response(status=status.HTTP_204_NO_CONTENT)

class AvailableReagentsCategoryView(APIView):
    """
    Returns a json object keyed by reagent or reagent group name with their
    respective category as value
    """

    def get(self,request):
        return Response(ViewHelpers.available_reagents_category())

