from .models import Page, Forsiduhlutar
from nafnid_django_admin.models import *
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from rest_framework.response import Response
from drf_multiple_model.views import ObjectMultipleModelAPIView
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
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
                url = url + '/'
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


''' =========================== /VEFUR =========================== '''


class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 1


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class PDF(viewsets.ReadOnlyModelViewSet):
    serializer_class = PDFSerializer

    def get_queryset(self):
        return PdfSkrarFinnur.objects.all()


class Textaleit(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrnefnaskrarMinniSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q')
        m = self.request.query_params.get('m')
        sveitarfelag = self.request.query_params.get('sveitarfelag')
        sysla = self.request.query_params.get('sysla')
        hreppur = self.request.query_params.get('hreppur')
        tegund = self.request.query_params.get('tegund')
        queryset = []

        if query is not None:
            reg = query.replace('*', '.*?')
            queryset = Ornefnaskrar.objects.filter(Q(pdf_skra_id__ocr_text__iregex=reg))

            if tegund:
                queryset = queryset.filter(Q(tegund__id=tegund))

            if sysla and sveitarfelag:
                queryset = queryset.filter(Q(sysla__id=sysla) | Q(sveitarfelag__id=sveitarfelag))
            elif sysla:
                queryset = queryset.filter(Q(sysla__id=sysla))
            elif sveitarfelag:
                queryset = queryset.filter(Q(sveitarfelag__id=sveitarfelag))
            elif hreppur:
                queryset = queryset.filter(Q(hreppur__id=hreppur))

        return queryset


class Ornefnaleit(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrnefnaleitSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q')
        m = self.request.query_params.get('m')
        sveitarfelag = self.request.query_params.get('sveitarfelag')
        sysla = self.request.query_params.get('sysla')
        hreppur = self.request.query_params.get('hreppur')
        tegund = self.request.query_params.get('tegund')
        queryset = []

        if query is not None:
            if '*' in query:
                reg = query.replace('*', '.*?')
                queryset = Ornefnapakki.objects.filter(Q(ornefni__regex=reg)).distinct('ornefni', 'ornefnaskra').order_by('ornefni', 'ornefnaskra')
            else:
                if m == 'er':
                    queryset = Ornefnapakki.objects.filter(Q(ornefni_iexact=query)).distinct('ornefni', 'ornefnaskra').order_by('ornefni', 'ornefnaskra')
                elif m == 'endar':
                    queryset = Ornefnapakki.objects.filter(Q(ornefni__iendswith=query)).distinct('ornefni', 'ornefnaskra').order_by('ornefni', 'ornefnaskra')
                elif m == 'byrjar':
                    queryset = Ornefnapakki.objects.filter(Q(ornefni__istartswith=query)).distinct('ornefni', 'ornefnaskra').order_by('ornefni', 'ornefnaskra')
                else:
                    queryset = Ornefnapakki.objects.filter(Q(ornefni__contains=query)).distinct('ornefni', 'ornefnaskra').order_by('ornefni', 'ornefnaskra')

            if tegund:
                queryset = queryset.filter(Q(ornefnaskra__tegund__id=tegund))

            if sysla and sveitarfelag:
                queryset = queryset.filter(Q(sysla__id=sysla) | Q(sveitarfelag__id=sveitarfelag))
            elif sysla:
                queryset = queryset.filter(Q(sysla__id=sysla))
            elif sveitarfelag:
                queryset = queryset.filter(Q(sveitarfelag__id=sveitarfelag))
            elif hreppur:
                queryset = queryset.filter(Q(hreppur__id=hreppur))

        return queryset


class Baejaleit(viewsets.ReadOnlyModelViewSet):
    serializer_class = BaejaleitSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q')
        m = self.request.query_params.get('m')
        sveitarfelag = self.request.query_params.get('sveitarfelag')
        sysla = self.request.query_params.get('sysla')
        hreppur = self.request.query_params.get('hreppur')

        if query is not None:
            if '*' in query:
                reg = query.replace('*', '.*?')
                queryset = BaejatalBaeir.objects.filter(Q(baejarnafn__regex=reg)).order_by('baejarnafn')
            else:
                if m == 'byrjar':
                    queryset = BaejatalBaeir.objects.filter(Q(baejarnafn__istartswith=query)).order_by('baejarnafn')
                elif m == 'endar':
                    queryset = BaejatalBaeir.objects.filter(Q(baejarnafn__iendswith=query)).order_by('baejarnafn')
                elif m == 'er':
                    queryset = BaejatalBaeir.objects.filter(Q(baejarnafn__iexact=query)).order_by('baejarnafn')
                else:
                    queryset = BaejatalBaeir.objects.filter(Q(baejarnafn__contains=query)).order_by('baejarnafn')

            if sysla and sveitarfelag:
                queryset = queryset.filter(Q(sysla__id=sysla) | Q(sveitarfelag__id=sveitarfelag))
            elif sysla:
                queryset = queryset.filter(Q(sysla__id=sysla))
            elif sveitarfelag:
                queryset = queryset.filter(Q(sveitarfelag__id=sveitarfelag))
            elif hreppur:
                queryset = queryset.filter(Q(hreppur__id=hreppur))

        return queryset


class Siur(ObjectMultipleModelAPIViewSet):
    pagination_class = None

    def get_querylist(self):
        query = self.request.query_params.get('q')
        m = self.request.query_params.get('m')
        querylist = []
        if query is not None:
            if '*' in query:
                reg = query.replace('*', '.*?')

                querylist = [
                    {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__regex=reg)).distinct('sysla'), 'serializer_class': SiaBaejaleitSyslur, 'label': 'baeir_syslur'},
                    {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__regex=reg)).distinct('sveitarfelag'), 'serializer_class': SiaBaejaleitSveitarfelog, 'label': 'baeir_sveitarfelog'},
                    {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__regex=reg)).distinct('hreppur'), 'serializer_class': SiaBaejaleitHreppar, 'label': 'baeir_hreppar'},
                    {'queryset': Ornefnapakki.objects.filter(Q(ornefni__regex=reg)).distinct('sysla'), 'serializer_class': SiaOrnefnaleitSyslur, 'label': 'ornefni_syslur'},
                    {'queryset': Ornefnapakki.objects.filter(Q(ornefni__regex=reg)).distinct('sveitarfelag'), 'serializer_class': SiaOrnefnaleitSveitarfelog, 'label': 'ornefni_sveitarfelog'},
                    {'queryset': Ornefnapakki.objects.filter(Q(ornefni__regex=reg)).distinct('hreppur'), 'serializer_class': SiaOrnefnaleitHreppar, 'label': 'ornefni_hreppar'},
                    {'queryset': Ornefnapakki.objects.filter(Q(ornefni__regex=reg)).distinct('ornefnaskra__tegund').values(tegund=F('ornefnaskra__tegund__tegund'), tegund_id=F('ornefnaskra__tegund__id')), 'serializer_class': SiaOrnefnaleitTegundir, 'label': 'ornefni_tegundir'},
                    {'queryset': Tegundir.objects.all(), 'serializer_class': TegundSerializer, 'label': 'allar_tegundir'}
                ]
            else:

                if m == 'byrjar':
                    querylist = [
                        {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__istartswith=query)).distinct('sysla'), 'serializer_class': SiaBaejaleitSyslur, 'label': 'baeir_syslur'},
                        {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__istartswith=query)).distinct('sveitarfelag'), 'serializer_class': SiaBaejaleitSveitarfelog, 'label': 'baeir_sveitarfelog'},
                        {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__istartswith=query)).distinct('hreppur'), 'serializer_class': SiaBaejaleitHreppar, 'label': 'baeir_hreppar'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__istartswith=query)).distinct('sysla'), 'serializer_class': SiaOrnefnaleitSyslur, 'label': 'ornefni_syslur'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__istartswith=query)).distinct('sveitarfelag'), 'serializer_class': SiaOrnefnaleitSveitarfelog, 'label': 'ornefni_sveitarfelog'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__istartswith=query)).distinct('hreppur'), 'serializer_class': SiaOrnefnaleitHreppar, 'label': 'ornefni_hreppar'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__istartswith=query)).distinct('ornefnaskra__tegund').values(tegund=F('ornefnaskra__tegund__tegund'), tegund_id=F('ornefnaskra__tegund__id')), 'serializer_class': SiaOrnefnaleitTegundir, 'label': 'ornefni_tegundir'},
                        {'queryset': Tegundir.objects.all(), 'serializer_class': TegundSerializer, 'label': 'allar_tegundir'}
                    ]
                elif m == 'endar':
                    querylist = [
                        {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__iendswith=query)).distinct('sysla'), 'serializer_class': SiaBaejaleitSyslur, 'label': 'baeir_syslur'},
                        {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__iendswith=query)).distinct('sveitarfelag'), 'serializer_class': SiaBaejaleitSveitarfelog, 'label': 'baeir_sveitarfelog'},
                        {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__iendswith=query)).distinct('hreppur'), 'serializer_class': SiaBaejaleitHreppar, 'label': 'baeir_hreppar'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__iendswith=query)).distinct('sysla'), 'serializer_class': SiaOrnefnaleitSyslur, 'label': 'ornefni_syslur'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__iendswith=query)).distinct('sveitarfelag'), 'serializer_class': SiaOrnefnaleitSveitarfelog, 'label': 'ornefni_sveitarfelog'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__iendswith=query)).distinct('hreppur'), 'serializer_class': SiaOrnefnaleitHreppar, 'label': 'ornefni_hreppar'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__iendswith=query)).distinct('ornefnaskra__tegund').values(tegund=F('ornefnaskra__tegund__tegund'), tegund_id=F('ornefnaskra__tegund__id')), 'serializer_class': SiaOrnefnaleitTegundir, 'label': 'ornefni_tegundir'},
                        {'queryset': Tegundir.objects.all(), 'serializer_class': TegundSerializer, 'label': 'allar_tegundir'}
                    ]
                elif m == 'er':
                    querylist = [
                        {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__iexact=query)).distinct('sysla'), 'serializer_class': SiaBaejaleitSyslur, 'label': 'baeir_syslur'},
                        {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__iexact=query)).distinct('sveitarfelag'), 'serializer_class': SiaBaejaleitSveitarfelog, 'label': 'baeir_sveitarfelog'},
                        {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__iexact=query)).distinct('hreppur'), 'serializer_class': SiaBaejaleitHreppar, 'label': 'baeir_hreppar'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__iexact=query)).distinct('sysla'), 'serializer_class': SiaOrnefnaleitSyslur, 'label': 'ornefni_syslur'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__iexact=query)).distinct('sveitarfelag'), 'serializer_class': SiaOrnefnaleitSveitarfelog, 'label': 'ornefni_sveitarfelog'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__iexact=query)).distinct('hreppur'), 'serializer_class': SiaOrnefnaleitHreppar, 'label': 'ornefni_hreppar'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__iexact=query)).distinct('ornefnaskra__tegund').values(tegund=F('ornefnaskra__tegund__tegund'), tegund_id=F('ornefnaskra__tegund__id')), 'serializer_class': SiaOrnefnaleitTegundir, 'label': 'ornefni_tegundir'},
                        {'queryset': Tegundir.objects.all(), 'serializer_class': TegundSerializer, 'label': 'allar_tegundir'}
                    ]
                else:
                    querylist = [
                        {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__contains=query)).distinct('sysla'), 'serializer_class': SiaBaejaleitSyslur, 'label': 'baeir_syslur'},
                        {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__contains=query)).distinct('sveitarfelag'), 'serializer_class': SiaBaejaleitSveitarfelog, 'label': 'baeir_sveitarfelog'},
                        {'queryset': BaejatalBaeir.objects.filter(Q(baejarnafn__contains=query)).distinct('hreppur'), 'serializer_class': SiaBaejaleitHreppar, 'label': 'baeir_hreppar'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__contains=query)).distinct('sysla'), 'serializer_class': SiaOrnefnaleitSyslur, 'label': 'ornefni_syslur'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__contains=query)).distinct('sveitarfelag'), 'serializer_class': SiaOrnefnaleitSveitarfelog, 'label': 'ornefni_sveitarfelog'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__contains=query)).distinct('hreppur'), 'serializer_class': SiaOrnefnaleitHreppar, 'label': 'ornefni_hreppar'},
                        {'queryset': Ornefnapakki.objects.filter(Q(ornefni__contains=query)).distinct('ornefnaskra__tegund').values(tegund=F('ornefnaskra__tegund__tegund'), tegund_id=F('ornefnaskra__tegund__id')), 'serializer_class': SiaOrnefnaleitTegundir, 'label': 'ornefni_tegundir'},
                        {'queryset': Tegundir.objects.all(), 'serializer_class': TegundSerializer, 'label': 'allar_tegundir'}
                    ]

        return querylist


class Uuid(viewsets.ReadOnlyModelViewSet):
    serializer_class = Uuid

    def get_queryset(self):
        query = self.request.query_params.get('q')
        m = self.request.query_params.get('m')
        tegund = self.request.query_params.get('tegund')
        sveitarfelag = self.request.query_params.get('sveitarfelag')
        sysla = self.request.query_params.get('sysla')
        hreppur = self.request.query_params.get('hreppur')

        if query is not None:
            if '*' in query:
                reg = query.replace('*', '.*?')
                queryset = Ornefnapakki.objects.filter(Q(ornefni__regex=reg)).filter(Q(uuid__isnull=False))
            else:
                if m == 'byrjar':
                    queryset = Ornefnapakki.objects.filter(Q(ornefni__istartswith=query)).filter(Q(uuid__isnull=False))
                elif m == 'endar':
                    queryset = Ornefnapakki.objects.filter(Q(ornefni__iendswith=query)).filter(Q(uuid__isnull=False))
                elif m == 'er':
                    queryset = Ornefnapakki.objects.filter(Q(ornefni__iexact=query)).filter(Q(uuid__isnull=False))
                else:
                    queryset = Ornefnapakki.objects.filter(Q(ornefni__contains=query)).filter(Q(uuid__isnull=False))

            if tegund:
                queryset = queryset.filter(Q(ornefnaskra__tegund__id=tegund))

            if sysla and sveitarfelag:
                queryset = queryset.filter(Q(sysla__id=sysla) | Q(sveitarfelag__id=sveitarfelag))
            elif sysla:
                queryset = queryset.filter(Q(sysla__id=sysla))
            elif sveitarfelag:
                queryset = queryset.filter(Q(sveitarfelag__id=sveitarfelag))
            elif hreppur:
                queryset = queryset.filter(Q(hreppur__id=hreppur))

        return queryset


class OrnefniViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrnefninSerializer

    def get_queryset(self):
        return Ornefni.objects.order_by('ornefni').all()


class OrnefnaskrarViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Ornefnaskrar.objects.all().order_by('ornefnaskrarbaeir__baer__baejarnafn')
        if self.action == 'list':
            self.serializer_class = OrnefnaskrarMinniSerializer
        else:
            self.serializer_class = OrnefnaskrarSerializer
        return queryset


class BaeirViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BaeirSerializer

    def get_queryset(self):
        queryset = BaejatalBaeir.objects.all().order_by('baejarnafn')
        if self.action == 'list':
            self.serializer_class = BaeirSerializer
        else:
            self.serializer_class = BaerSerializer
        return queryset


class HreppurViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HreppurSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = BaejatalSveitarfelogGomul.objects.filter(id=pk)

        return queryset


class HrepparViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HrepparSerializer

    def get_queryset(self):
        if self.action == 'list':
            queryset = BaejatalSveitarfelogGomul.objects.all().order_by('nafn')
            self.serializer_class = HrepparSerializer
        else:
            queryset = BaejatalBaeirHreppar.objects.select_related('baer').select_related('baer__sysla').all()
            self.serializer_class = HreppurBaeirSerializer

        return queryset


class SveitarfelogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SveitarfelogSerializer

    def get_queryset(self):
        if self.action == 'list':
            queryset = BaejatalSveitarfelogNy.objects.all().order_by('nafn')
            self.serializer_class = SveitarfelogSerializer
        else:
            queryset = BaejatalBaeirSveitarfelog.objects.select_related('baer').select_related('baer__sysla').all()
            self.serializer_class = SveitarfelogBaeirSerializer

        return queryset


class SyslurViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SyslurSerializer

    def get_queryset(self):
        if self.action == 'list':
            queryset = BaejatalSyslur.objects.all()
            self.serializer_class = SyslurSerializer
        else:
            pk = self.kwargs['pk']
            queryset = BaejatalSyslur.objects.filter(id=pk).all()
            self.serializer_class = SyslaHrepparSerializer
        return queryset


class EinstaklingarViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EinstaklingarSerializer

    def get_queryset(self):
        if self.action == 'list':
            queryset = Einstaklingar.objects.all().order_by('nafn')
            self.serializer_class = EinstaklingarSerializer
        else:
            pk = self.kwargs['pk']
            queryset = Einstaklingar.objects.filter(id=pk).all()
            self.serializer_class = EinstaklingurSerializer
        return queryset

class OrnefnaskrarEinstaklingsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrnefnaskrarEinstaklingsSerializer

    def get_queryset(self):
        if self.action == 'list':
            queryset = Einstaklingar.objects.all().order_by('nafn')
            self.serializer_class = EinstaklingarSerializer
        else:
            pk = self.kwargs['pk']
            queryset = Einstaklingar.objects.filter(id=pk).all()
            self.serializer_class = OrnefnaskrarEinstaklingsSerializer
        return queryset


class AbendingarViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Abendingar.objects.none()
	serializer_class = AbendingarSendSerializer

	def retrieve(self, request, pk=None):
		return Response({})

	def get_queryset(self):
		queryset = Abendingar.objects.none()

		return queryset

	def post(self, request):
		serializer = AbendingarSendSerializer(data=request.data)

		if serializer.is_valid():
			abending = Abendingar(
				nafn=request.data['nafn'],
				netfang=request.data['netfang'],
				simanumer=request.data['simanumer'],
				skilabod=request.data['skilabod'],
				entity_type=request.data['entity_type'],
				entity_id=request.data['entity_id']
			)

			abending.save(force_insert=True)

			return Response({
				'success': 'fyrirspurn send',
			})
		else:
			return Response({'error': 'invalid data'})
