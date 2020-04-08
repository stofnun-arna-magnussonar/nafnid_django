from .models import Page, Forsiduhlutar
from rest_framework import viewsets, permissions, mixins, status
from .serializers import PageSerializer, SinglePageSerializer, ForsiduhlutarSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.db.models import Sum
from django.db.models import F
from django.db.models import Q
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from datetime import datetime, timedelta
from os import listdir, path

import json

class PagesViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = PageSerializer

	def get_queryset(self):
		url = self.request.query_params.get('url', None)
		if url is not None:
			if not url.endswith('/'):
				url = url+'/'
			self.serializer_class = SinglePageSerializer

			queryset = Page.objects.filter(url__iexact=url, use_as_link=False)
		else:
			self.serializer_class = PageSerializer

			queryset = Page.objects.all().filter(in_menu=True)

			site = self.request.query_params.get('site', None)
			if site is not None:
				queryset = queryset.filter(site=site)

			queryset = queryset.order_by('order')

		return queryset

class ForsiduhlutarViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = ForsiduhlutarSerializer

	def get_queryset(self):
		queryset = Forsiduhlutar.objects.all()

		site = self.request.query_params.get('site', None)
		if site is not None:
			queryset = queryset.filter(site=site)

		return queryset


