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
from django.conf.urls import url
from django.contrib import admin

from rest_framework import routers

from app.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

router = routers.DefaultRouter()

router.register(r'api/experiments', ExperimentViewSet)
router.register(r'api/concentrations', ConcentrationViewSet)
router.register(r'api/concretereagents', ConcreteReagentViewSet)
router.register(r'api/buffermixes', BufferMixViewSet)
router.register(r'api/mixedreagents', MixedReagentViewSet)
router.register(r'api/placeholderreagents', PlaceholderReagentViewSet)
router.register(r'api/mastermixes', MasterMixViewSet)
router.register(r'api/genes', GeneViewSet)
router.register(r'api/organisms', OrganismViewSet)
router.register(r'api/primers', PrimerViewSet)
router.register(r'api/primerpairs', PrimerPairViewSet)
router.register(r'api/primerkits', PrimerKitViewSet)
router.register(r'api/args', ArgViewSet)
router.register(r'api/strains', StrainViewSet)
router.register(r'api/strainkits', StrainKitViewSet)
router.register(r'api/cyclingpatterns', CyclingPatternViewSet)
router.register(r'api/allocrules', AllocRuleViewSet)
router.register(r'api/allocationinstructions', AllocationInstructionsViewSet)
router.register(r'api/plates', PlateViewSet)
router.register(r'api/experiments', ExperimentViewSet)

urlpatterns += router.urls
