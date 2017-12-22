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

from app.views import ConcentrationViewSet
from app.views import ConcreteReagentSet

from app.views import PrimerViewSet
from app.views import PrimerPairViewSet
from app.views import OrganismViewSet
from app.views import ArgViewSet
from app.views import StrainViewSet
from app.views import CyclingPatternViewSet
from app.views import ConcentrationViewSet

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

router = routers.DefaultRouter()

router.register(r'api/concentrations', ConcentrationViewSet)
router.register(r'api/concentrations', ConcreteReagentViewSet)

router.register(r'api/primers', PrimerViewSet)
router.register(r'api/primer-pairs', PrimerPairViewSet)
router.register(r'api/organisms', OrganismViewSet)
router.register(r'api/args', ArgViewSet)
router.register(r'api/strains', StrainViewSet)
router.register(r'api/cycling-patterns', CyclingPatternViewSet)

urlpatterns += router.urls
