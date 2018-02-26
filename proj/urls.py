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
from django.urls import re_path
from django.contrib import admin

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


from app.views import *

# URL config for custom views.
urlpatterns = [
    re_path(r'^admin/', admin.site.urls),

    # Contrary to the documentation, it seems that we must set the name kwarg
    # explicitly to enable reverse-url lookups to work - when they are required
    # by HyperlinkedModelSerializer nested serializer fields.
    # re_path(r'^api/rulelist-detail/(?P<pk>[0-9]+)/$',
    #     RuleListDetail.as_view(), name='rulelist-detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)

# Automated config of URLs for the default ViewSet-derived views.
router = routers.DefaultRouter()

router.register(r'api/experiments', ExperimentViewSet)
router.register(r'api/compositions', CompositionViewSet)
router.register(r'api/measures', MeasureViewSet)
router.register(r'api/genes', GeneViewSet)
router.register(r'api/organisms', OrganismViewSet)
router.register(r'api/primers', PrimerViewSet)
router.register(r'api/primerpairs', PrimerPairViewSet)
router.register(r'api/args', ArgViewSet)
router.register(r'api/strains', StrainViewSet)
router.register(r'api/cyclingpatterns', CyclingPatternViewSet)
router.register(r'api/experiments', ExperimentViewSet)

urlpatterns += router.urls
