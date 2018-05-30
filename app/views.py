from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .serializers import *
from .view_helpers import ViewHelpers
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from app.experiment_results.qpcr_results_processor import QpcrResultsProcessor
from app.experiment_results.labchip_results_processor import LabChipResultsProcessor
from app.experiment_results.well_results_processor import WellResultsAggregation
from django.db import connection
from app.experiment_results.result_aggregation_query import GroupByIDASSAY
import ast

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
        results_processor = QpcrResultsProcessor(plate_name=plate_name,
                                                 experiment_name=experiment_name,
                                                 category_tags=['assay',
                                                                'template',
                                                                'human'])
        results,reagents_used,reagent_group_used = \
            results_processor.parse_qpcr_file(file)
        for record in results:
            qpcr_serializer = self.get_serializer(data=record)
            qpcr_serializer.is_valid(raise_exception=True)
            instance = qpcr_serializer.save()
            if instance.qpcr_well in reagents_used:
                for reagent in reagents_used[instance.qpcr_well]:
                    reagent['well'] = instance.id
                    reagent_serializer = ReagentWellLookupSerializer(
                        data=reagent)
                    reagent_serializer.is_valid(raise_exception=True)
                    reagent_serializer.save()
            if instance.qpcr_well in reagent_group_used :
                for reagent_group in reagent_group_used[instance.qpcr_well]:
                    reagent_group['well']=instance.id
                    reagent_group_serializer = ReagentGroupWellLookupSerializer(
                        data=reagent_group)
                    reagent_group_serializer.is_valid(raise_exception=True)
                    reagent_group_serializer.save()

        return Response(qpcr_serializer.data)



class LabChipResultsViewSet(viewsets.ModelViewSet):

    queryset = LabChipResultsModel.objects.all()
    serializer_class = LabChipResultsSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES['file']
        plate_name = request.POST['plateName']
        experiment_name = request.POST['experimentName']
        labchip_processor = LabChipResultsProcessor(
            plate_name=plate_name, experiment_name=experiment_name)
        labchip_results = labchip_processor.parse_labchip_file(file)
        serializer = self.get_serializer(data=labchip_results, many=True)
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


    def get(self,request):
        # Returns list of unique reagent group names in db
        return Response(ViewHelpers.group_names())

    def delete(self, request):
        # Its easier to implement this explicitly rather than trying to use
        # the serializer , because serializer demands all the fields whereas
        # we only need group name
        try:
            group_name = request.data['group_name']
            with transaction.atomic():
                ReagentGroupModel.objects.filter(group_name=group_name).delete()
        except :
            raise ValidationError('Invalid request;Please mention a group name')

        return Response(status=status.HTTP_204_NO_CONTENT)

class AvailableReagentsCategoryView(APIView):
    """
    Returns a json object keyed by reagent or reagent group name with their
    respective category as value
    """

    def get(self,request):
        return Response(ViewHelpers.available_reagents_category())

class WellResultsView(APIView):

    def get(self,request):
        experiment_id = request.query_params['expt']
        plate_id = request.query_params['plate_id']
        wells = ast.literal_eval(request.query_params['wells'])
        results = WellResultsAggregation.create_from_wells(experiment_id, plate_id,
                                                   wells)
        return Response(results)

class WellAggregationView(APIView):

    def get(self,request):
        with connection.cursor() as cursor:
            cursor.execute(GroupByIDASSAY)
            columns = [col[0] for col in cursor.description]
            return Response([
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ])