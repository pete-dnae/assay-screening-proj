from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .view_helpers import ViewHelpers
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from app.experiment_results.qpcr_results_loader import load_qpcr_results
from app.experiment_results.labchip_results_loader import load_labchip_results
from app.experiment_results.experiment_data_extractor import \
    get_wells_grouped_by_id_assay
from app.experiment_results.qpcr_well_aggregation import QpcrWellAggregation
from django.http import Http404
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
import ast

class ExperimentViewSet(viewsets.ModelViewSet):

    queryset = ExperimentModel.objects.all()
    serializer_class =  ExperimentSerializer
    lookup_value_regex = '[a-zA-Z0-9_ ]+'

class RulesScriptViewSet(viewsets.ModelViewSet):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ReagentCategoryModel.objects.all()
    serializer_class = ReagentCategorySerializer


class ReagentGroupViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ReagentGroupModel.objects.all()
    serializer_class = ReagentGroupSerializer


class ReagentGroupDetailsViewSet(viewsets.ModelViewSet):
    queryset = ReagentGroupDetailsModel.objects.all()
    serializer_class = ReagentGroupDetailsSerializer

class QpcrResultsViewSet(viewsets.ModelViewSet):

    queryset = QpcrResultsModel.objects.all()
    serializer_class = QpcrResultsSerializer

    def create(self, request, *args, **kwargs):
        """
        Reads the excel file in request and extracts necessary information
        from it using QpcrResultsProcessor

        Expects an excel file to be passed as a part of request
        """
        file = request.FILES['file']
        plate_name = request.POST['plateName']
        experiment_name = request.POST['experimentName']
        results = load_qpcr_results(experiment_name,plate_name,file)

        return Response(results)



class LabChipResultsViewSet(viewsets.ModelViewSet):

    queryset = LabChipResultsModel.objects.all()
    serializer_class = LabChipResultsSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES['file']
        plate_name = request.POST['plateName']
        experiment_name = request.POST['experimentName']
        results = load_labchip_results(experiment_name,plate_name,file)
        return Response(results)

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


class AvailableReagentsCategoryView(APIView):
    """
    Returns a json object keyed by reagent or reagent group name with their
    respective category as value
    """

    def get(self,request):
        return Response(ViewHelpers.available_reagents_category())

class WellResultsView(APIView):
    """
    Returns well results in the form of summary table ,master table and
    in data format edible for JavaScript graphs
    """

    def get(self,request):
        experiment_id = request.query_params['expt']
        plate_id = request.query_params['plate_id']
        wells = ast.literal_eval(request.query_params['wells'])
        qpcr_query_set=QpcrResultsModel.objects.filter(
            experiment_id=experiment_id, qpcr_plate_id=plate_id,
            qpcr_well__in=wells)
        if qpcr_query_set.exists():
            result = QpcrWellAggregation.create_from_query(qpcr_query_set)
            return Response(result)
        else:
            raise Http404


class WellAggregationView(APIView):

    def get(self,request):
        wells_by_id_assay = get_wells_grouped_by_id_assay()
        return Response(wells_by_id_assay)
