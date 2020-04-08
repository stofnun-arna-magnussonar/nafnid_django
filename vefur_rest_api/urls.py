from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from . import views

router = routers.DefaultRouter()
router.register(r'pages', views.PagesViewSet, base_name='pages')
router.register(r'front_sections', views.ForsiduhlutarViewSet, base_name='front_sections')

urlpatterns = [
	url(r'^', include(router.urls))
]
