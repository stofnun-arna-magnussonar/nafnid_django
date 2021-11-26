from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from . import views

router = routers.DefaultRouter()
router.register(r'ornefnaskrar', views.OrnefnaskrarViewSet, basename='ornefnaskrar_api')
router.register(r'ornefni', views.OrnefniViewSet, basename='ornefni_api')

router.register(r'ornefnaskrareinstaklings', views.OrnefnaskrarEinstaklingsViewSet, basename='ornefnaskrareinstaklings_api')

router.register(r'einstaklingar', views.EinstaklingarViewSet, basename='einstaklingar_api')
router.register(r'baeir', views.BaeirViewSet, basename='baeir_api')
router.register(r'hreppar', views.HrepparViewSet, basename='hreppar_api')
router.register(r'sveitarfelog', views.SveitarfelogViewSet, basename='sveitarfelog_api')
router.register(r'syslur', views.SyslurViewSet, basename='syslur_api')


urlpatterns = [
	url(r'^', include(router.urls)),

]
