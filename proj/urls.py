"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path,include
from django.contrib import admin

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from app.views import *

# URL config for custom views.
urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/allowed-names/$', AllowedNamesView.as_view()),
    re_path(r'^api/experiment-images/(?P<experiment_id>[a-zA-Z0-9_ ]+)$',
            ExperimentImagesView.as_view()),
    re_path(r'api/available-reagents-category$',
            AvailableReagentsCategoryView.as_view()),
    re_path(r'api/well-results/$',
            WellResultsView.as_view()),
    re_path(r'api/well-aggregate/$',WellAggregationView.as_view()),
    re_path(r'api/Mob2DslView/',Mob2DslView.as_view()),
    re_path(r'api/delete-qpcr/$',QpcrWellDeletionsView.as_view()),
    re_path(r'api/delete-labchip/$',LabChipWellDeletionsView.as_view()),
    re_path(r'^auth/obtain_token/', obtain_jwt_token),
    re_path(r'^auth/refresh_token/', refresh_jwt_token),
    re_path(r'^api/annotate-qpcr/',qPCRWellAnnotationsView.as_view()),
    re_path(r'^api/annotate-labchip/',LabChipWellAnnotationsView.as_view()),
    re_path(r'^api/bulk-load-reagents/',ReagentUploadView.as_view())
]
# Automated config of URLs for the default ViewSet-derived views.
router = routers.DefaultRouter()

router.register(r'api/experiments',ExperimentViewSet)
router.register(r'api/rule-scripts', RulesScriptViewSet)
router.register(r'api/reagents', ReagentViewSet)
router.register(r'api/reagent-categories', ReagentCategoryViewSet)
router.register(r'api/reagent-groups', ReagentGroupViewSet)
router.register(r'api/units', UnitViewSet)
router.register(r'api/qpcr-results',QpcrResultsViewSet)
router.register(r'api/labchip-results',LabChipResultsViewSet)
router.register(r'api/reagent-group-details',ReagentGroupDetailsViewSet)

urlpatterns = format_suffix_patterns(urlpatterns)


urlpatterns += router.urls
