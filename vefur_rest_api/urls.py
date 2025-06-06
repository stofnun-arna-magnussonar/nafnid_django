from django.urls import include, re_path
from django.urls import path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from . import views

router = routers.DefaultRouter()
router.register(r'pages', views.PagesViewSet, basename='pages')
router.register(r'front_sections', views.ForsiduhlutarViewSet, basename='front_sections')

router.register(r'oleit', views.Ornefnaleit, basename='oleit')
router.register(r'bleit', views.Baejaleit, basename='bleit')
router.register(r'geoleit', views.GeoleitView, basename='geoleit')
router.register(r'textaleit', views.Textaleit, basename='textaleit')


router.register(r'siur', views.Siur, basename='siur')
router.register(r'uuid', views.Uuid, basename='uuid')

router.register(r'ornefnaskrar', views.OrnefnaskrarViewSet, basename='ornefnaskrar')
router.register(r'ornefni', views.OrnefniViewSet, basename='ornefni')

router.register(r'ornefnaskrareinstaklings', views.OrnefnaskrarEinstaklingsViewSet, basename='ornefnaskrareinstaklings')

router.register(r'einstaklingar', views.EinstaklingarViewSet, basename='einstaklingar')
router.register(r'baeir', views.BaeirViewSet, basename='baeir')
router.register(r'hreppar', views.HrepparViewSet, basename='hreppar')
router.register(r'sveitarfelog', views.SveitarfelogViewSet, basename='sveitarfelog')
router.register(r'syslur', views.SyslurViewSet, basename='syslur')

router.register(r'greinar', views.ArticlesViewSet, basename='greinar')

router.register(r'nofn_islendinga/greinar', views.NofnIslendingaGreinarViewSet, basename='nofn_islendinga_greinar')
router.register(r'nofn_islendinga', views.NofnIslendingaNofnViewSet, basename='nofn_islendinga')

router.register(r'abending', views.AbendingarViewSet, basename='abending')

urlpatterns = [
	re_path(r'^', include(router.urls)),
]
