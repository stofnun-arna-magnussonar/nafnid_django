# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class Ornefnaskrar(models.Model):
	id = models.AutoField(primary_key=True)
	titill = models.CharField(max_length=300, blank=True, null=True)
	texti = models.TextField(blank=True, null=True)
	sysla = models.ForeignKey('BaejatalSyslur', models.DO_NOTHING, db_column='sysla', verbose_name='sýsla', blank=True, null=True)
	hreppur = models.ForeignKey('BaejatalSveitarfelogGomul', models.DO_NOTHING, db_column='hreppur', verbose_name='hreppur', blank=True, null=True)
	stafraent = models.BooleanField(blank=True, null=True, verbose_name='stafrænt?')
	pappir = models.BooleanField(blank=True, null=True, verbose_name='pappír?')
	pdf_skra_id = models.ForeignKey('PdfSkrarFinnur', models.DO_NOTHING, db_column='pdf_skra_id', verbose_name='pdf skrá', blank=True, null=True)
	artal_skrar = models.IntegerField(blank=True, null=True, verbose_name='ártal skrár')
	#pdf_skra = models.ForeignKey('PdfSkrarFinnur', models.DO_NOTHING, db_column='pdf_skra', verbose_name='pdf skrá', blank=True, null=True)

	tegund = models.ManyToManyField(
		'Tegundir',
		through='OrnefnaskrarTegundir',
		verbose_name = 'Tegundir skráningar'
	)

	stada = models.ManyToManyField(
		'Stada',
		through='OrnefnaskrarStada',
		verbose_name = 'Staða skráningar'
	)

	ornefni = models.ManyToManyField(
		'Ornefni',
		through='OrnefnaskrarOrnefni',
		verbose_name='Örnefni'
	)

	baeir = models.ManyToManyField(
		'BaejatalBaeir',
		through='OrnefnaskrarBaeir',
		verbose_name='bæir'
	)

	einstaklingar = models.ManyToManyField(
		'Einstaklingar',
		through='OrnefnaskrarEinstaklingar',
		verbose_name = 'einstaklingar'
	)

	class Meta:
		managed = False
		db_table = 'ornefnaskrar'
		verbose_name = 'skjal'
		verbose_name_plural = 'skjöl'

	def __str__(self):
		return self.titill

	def get_absolute_url(self):
		return reverse('ornefnaskra_detail', args=[str(self.id)])

	def ornefna_link(self):
		orn = Ornefni.objects.filter(ornefnaskra=self.pk, okay__exact=False)
		if orn.values():
			map_html = '<a class="grp-button" href="/admin/nafnid_django_admin/ornefni/?ornefnaskra__id__exact={0}">Óyfirfarin örnefni</a>'
			return format_html(map_html, str(self.id))

	ornefna_link.short_description = 'örnefni'
	ornefna_link.allow_tags = True

	def fjoldi_ornefna(self):
		orn = Ornefni.objects.filter(ornefnaskra=self.pk)
		return len(orn)

	fjoldi_ornefna.short_description = 'fjöldi örnefna'

	def lmi(self):
		salt = [82, 2, 76, 23, 42, 31, 25, 12, 52, 15, 56, 54, 18, 4, 70, 97, 57, 35, 78, 88, 60, 40, 51, 11, 58, 20, 85, 1, 89, 5, 7, 14]
		m = 0
		ds = str.encode(str(self.id))
		for i in range(min(len(str(self.id)), len(salt))):
			m = m + ds[i] * salt[i]
		return "//atlas.lmi.is/ornefnaritill/?nafnid="+str(self.id)+"&var="+str(m)

class OrnefnaskrarBaeir(models.Model):
	ornefnaskra = models.ForeignKey('Ornefnaskrar', models.DO_NOTHING, db_column='ornefnaskra', verbose_name='örnefnaskrá')
	baer = models.ForeignKey('BaejatalBaeir', models.DO_NOTHING, db_column='baer', verbose_name='bær')
	tegund = models.CharField(max_length=100, blank=True, null=True, verbose_name='tegund')

	class Meta:
		managed = False
		db_table = 'ornefnaskrar_baeir'
		verbose_name = 'bær'
		verbose_name_plural = 'bæir'


class BaeirOrnefnaskrar(models.Model):
	ornefnaskra = models.ForeignKey('Ornefnaskrar', models.DO_NOTHING, db_column='ornefnaskra', verbose_name='örnefnaskrá')
	baer = models.ForeignKey('BaejatalBaeir', models.DO_NOTHING, db_column='baer', verbose_name='bær')
	tegund = models.CharField(max_length=100, blank=True, null=True, verbose_name='tegund')

	class Meta:
		managed = False
		db_table = 'ornefnaskrar_baeir'
		verbose_name = 'örnefnaskra'
		verbose_name_plural = 'örnefnaskrar'


class Hlutverk(models.Model):
	hlutverk = models.CharField(max_length=150, blank=False, null=False)

	class Meta:
		managed = False
		db_table = 'hlutverk'
		verbose_name = 'hlutverk'
		verbose_name_plural = 'hlutverk'

	def __str__(self):
		return self.hlutverk


class OrnefnaskrarEinstaklingar(models.Model):
	einstaklingur = models.ForeignKey('Einstaklingar', models.DO_NOTHING, db_column='einstaklingur', verbose_name='einstaklingur')
	ornefnaskra = models.ForeignKey('Ornefnaskrar', models.DO_NOTHING, db_column='ornefnaskra', verbose_name='örnefnaskrá')
	#hlutverk = models.CharField(max_length=200, blank=True, null=True, verbose_name='hlutverk', choices=[('skrasetjari', 'Skrásetjari'), ('heimildamadur', 'Heimildamaður'), ('starfsmadur', 'Starfsmaður Örnefnastofnunar'), ('kortagerð', 'Kortagerð')])
	hlutverk = models.ForeignKey('Hlutverk', models.DO_NOTHING, db_column='hlutv')

	class Meta:
		managed = False
		db_table = 'ornefnaskrar_einstaklingar'
		verbose_name = 'einstaklingur'
		verbose_name_plural = 'einstaklingar'


class EinstaklingarOrnefnaskrar(models.Model):
	einstaklingur = models.ForeignKey('Einstaklingar', models.DO_NOTHING, db_column='einstaklingur', verbose_name='einstaklingur')
	ornefnaskra = models.ForeignKey('Ornefnaskrar', models.DO_NOTHING, db_column='ornefnaskra', verbose_name='örnefnaskrá')
	#hlutverk = models.CharField(max_length=200, blank=True, null=True, verbose_name='hlutverk', choices=[('skrasetjari', 'Skrásetjari'), ('heimildamadur', 'Heimildamaður'), ('starfsmadur', 'Starfsmaður Örnefnastofnunar'), ('kortagerð', 'Kortagerð')])
	hlutverk = models.ForeignKey('Hlutverk', models.DO_NOTHING, db_column='hlutv')


	class Meta:
		managed = False
		db_table = 'ornefnaskrar_einstaklingar'
		verbose_name = 'örnefnaskrá'
		verbose_name_plural = 'örnefnaskrár'

	def __str__(self):
		return self.hlutverk.hlutverk


'''class Ornefni(models.Model):
	ornefni = models.CharField(max_length=300, blank=True, null=True, verbose_name='örnefni')
	lat = models.FloatField(blank=True, null=True)
	lon = models.FloatField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'ornefni'
		verbose_name = 'örnefni'
		verbose_name_plural = 'örnefni'

	def __str__(self):
		return self.ornefni'''


class Ornefni(models.Model):
	id = models.AutoField(primary_key=True)
	ornefni = models.CharField(max_length=300, blank=True, null=True, verbose_name='örnefni')
	samraemt = models.CharField(max_length=300, blank=True, null=True, verbose_name='samræmt')
	ornefnaskra = models.ForeignKey('Ornefnaskrar', models.DO_NOTHING, db_column='ornefnaskra', verbose_name='örnefnaskrá', blank=True, null=True, related_name='skra')
	pdf_skra_id = models.ForeignKey('PdfSkrarFinnur', models.DO_NOTHING, db_column='pdf_skra_id', verbose_name='PDF skrá', blank=True, null=True)
	lat = models.FloatField(blank=True, null=True)
	lon = models.FloatField(blank=True, null=True)
	okay = models.BooleanField(blank=True, null=True, verbose_name='Rétt?')
	tvitak = models.BooleanField(blank=True, null=True, verbose_name='Tvítekning?')
	uuid = models.CharField(max_length=36, blank=True, null=True, verbose_name='UUID Landmælinga')

	class Meta:
		managed = False
		db_table = 'ocr_ornefni'
		ordering = ('ornefni',)
		verbose_name = 'Ljóslesið örnefni'
		verbose_name_plural = 'Ljóslesin örnefni'

	def finnur(self):
		map_html = '<a class="grp-button" target="_blank" href="/admin/nafnid_django_admin/pdfskrarfinnur/{0}/change">{1}</a>'
		return format_html(map_html, str(self.pdf_skra_id.id), self.pdf_skra_id)

	finnur.short_description = 'PDF'

	def __str__(self):
		return self.ornefni

	def get_absolute_url(self):
		return reverse('ornefni_detail', args=[str(self.id)])


class OrnefnaskrarOrnefni(models.Model):
	ornefni = models.ForeignKey(Ornefni, on_delete=models.DO_NOTHING, db_column='ocrornefni', verbose_name='örnefni')
	ornefnaskra = models.ForeignKey(Ornefnaskrar, on_delete=models.DO_NOTHING, db_column='skra')

	class Meta:
		managed = False
		db_table = 'ornefnaskrar_ocrornefni'
		verbose_name = 'örnefni'
		verbose_name_plural = 'örnefni'


'''class OrnefnaskrarOrnefni(models.Model):
	ornefni = models.ForeignKey(Ornefni, on_delete=models.DO_NOTHING, db_column='ornefni', verbose_name='örnefni')
	skra = models.ForeignKey(Ornefnaskrar, on_delete=models.DO_NOTHING, db_column='skra')

	class Meta:
		managed = False
		db_table = 'ornefnaskrar_ornefni'
		verbose_name = 'örnefni'
		verbose_name_plural = 'örnefni'
'''


class Tegundir(models.Model):
	tegund = models.CharField(max_length=200, blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'tegundir'
		verbose_name = 'tegund'
		verbose_name_plural = 'tegundir'

	def __str__(self):
		return self.tegund


class OrnefnaskrarTegundir(models.Model):
	skra = models.ForeignKey(Ornefnaskrar, on_delete=models.DO_NOTHING, db_column='skra', verbose_name='skrá')
	tegund = models.ForeignKey(Tegundir, on_delete=models.DO_NOTHING, db_column='tegund')

	class Meta:
		managed = False
		db_table = 'ornefnaskrar_tegundir'
		verbose_name = 'tegund skjals'
		verbose_name_plural = 'tegund skjals'


class Stada(models.Model):
	stada = models.CharField(max_length=200, blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'stada'
		verbose_name = 'stada'
		verbose_name_plural = 'stöður'

	def __str__(self):
		return self.stada


class OrnefnaskrarStada(models.Model):
	skra = models.ForeignKey(Ornefnaskrar, on_delete=models.DO_NOTHING, db_column='skra', verbose_name='skrá')
	stada = models.ForeignKey(Stada, on_delete=models.DO_NOTHING, db_column='stada')
	athugasemd = models.TextField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'ornefnaskrar_stada'
		verbose_name = 'staða skjals'
		verbose_name_plural = 'staða skjals'


class OnFileField(models.FileField):
	def __init__(self, *args, **kwargs):
		super(OnFileField, self).__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):
		data = super(OnFileField, self).clean(*args, **kwargs)
		data.name = str(data.name.encode('ascii', 'ignore'))
		return data


#class Skraavensl(models.Model):


class PdfSkrarFinnur(models.Model):
	#slod = models.CharField(max_length=500, blank=False, null=False, verbose_name='slóð')
	sysla_id = models.IntegerField(blank=True, null=True, verbose_name='auðkenni sýslu')
	hreppur_id = models.IntegerField(blank=True, null=True, verbose_name='auðkenni hrepps')
	sysla = models.CharField(max_length=300, blank=True, null=True, verbose_name='sýsla (samkvæmt Finni)')
	hreppur = models.CharField(max_length=300, blank=True, null=True, verbose_name='hreppur (samkvæmt Finni)')
	bt_hreppur = models.ForeignKey('BaejatalSveitarfelogGomul', models.DO_NOTHING, db_column='bt_hreppur', verbose_name='sveitarfélag (bæjatal, 1970)')
	bt_sysla = models.ForeignKey('BaejatalSyslur', models.DO_NOTHING, db_column='bt_sysla', verbose_name='sýsla (bæjatal)')
	slod = models.FileField(upload_to='nyskannad/', max_length=500, verbose_name='pdf skrá')
	ocr_text = models.TextField(blank=True, null=True, verbose_name='ljóslesinn texti')
	artal_skrar = models.IntegerField(blank=True, null=True, verbose_name='ártal skrár')
	artal_stadfest = models.BooleanField(blank=True, null=True, verbose_name='staðfest ártal?')
	handrit = models.BooleanField(blank=True, null=True, verbose_name='handrit')
	handrit_orn = models.BooleanField(blank=True, null=True, verbose_name='örnefnaskrá fylgir')
	rannsakad = models.BooleanField(blank=True, null=True, verbose_name='rannsakað?')
	ornefni_vantar = models.BooleanField(blank=True, null=True, verbose_name='örnefni vantar')

	def hastext(self):
		if self.ocr_text:
			return 'Ja'
		else:
			return 'Nei'
	hastext.short_description = 'Með texta?'

	def file_tag(self):
		#	<a href="http://nidhoggur.rhi.hi.is/nafnid-media/uploads/{0}">Slóð á skrá</a>
		map_html = """
			<embed src="https://nafnid.arnastofnun.is/media/uploads/{0}" width="100%" height="800">
		"""

		return format_html(map_html,
			self.slod
		)

	file_tag.short_description = 'PdF'
	file_tag.allow_tags = True

	def pdf_url(self):
		map_html = 'https://nafnid.arnastofnun.is/media/uploads/{0}'
		return format_html(map_html,self.slod)

	def __str__(self):
		return self.slod.name

	def fjoldi_ornefna(self):
		orn = Ornefni.objects.filter(pdf_skra_id=self.pk)
		return len(orn)

	fjoldi_ornefna.short_description = 'fjöldi örnefna'

	class Meta:
		managed = False
		db_table = 'pdf_skrar_finnur'
		verbose_name = 'pdf skrá'
		verbose_name_plural = 'pdf skrár'

class BaejatalTegund(models.Model):
	tegund = models.CharField(max_length=300, blank=False, null=False, verbose_name='tegund')

	def __str__(self):
		return self.tegund

	class Meta:
		managed = False
		db_table = 'baejatal_tegund'
		verbose_name = 'tegund svæðis'
		verbose_name_plural = 'tegundir svæða'
		ordering = ['tegund']

class BaejatalBaeir(models.Model):
	id = models.AutoField(primary_key=True)
	baejarnafn = models.CharField(max_length=85, blank=True, null=True, verbose_name='heiti')
	samraemt = models.CharField(max_length=85, blank=True, null=True, verbose_name='samræmt')
	sveitarfelag = models.ForeignKey('BaejatalSveitarfelogNy', models.DO_NOTHING, db_column='nuv_sveitarf', verbose_name='núverandi sveitarfélag')
	hreppur = models.ForeignKey('BaejatalSveitarfelogGomul', models.DO_NOTHING, db_column='gamalt_sveitarf', verbose_name='sveitarfélag (1970)')
	sysla = models.ForeignKey('BaejatalSyslur', models.DO_NOTHING, db_column='sysla', verbose_name='sýsla')
	tegund = models.ForeignKey('BaejatalTegund', models.DO_NOTHING, null=True, blank=True)
	lbs_lykill = models.CharField(max_length=50, blank=True, null=True, verbose_name='lykill landsbókasafns')
	lat = models.FloatField(blank=True, null=True)
	lng = models.FloatField(blank=True, null=True)
	sveitarf_temp = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.baejarnafn+', '+str(self.sveitarfelag)+', '+str(self.sysla)

	def hnitsett(self):
		if self.lat:
			if self.lat > 0:
				return 'Ja'
			else:
				return 'Nei'

	def fjoldi_skjala(self):
		return OrnefnaskrarBaeir.objects.filter(baer=self.pk).count()

	class Meta:
		managed = False
		db_table = 'baejatal_baeir'
		#ordering = ('baejarnafn',)
		verbose_name = 'svæði'
		verbose_name_plural = 'svæði'

	def get_absolute_url(self):
		return reverse('baer_detail', args=[str(self.id)])


class BaejatalSveitarfelogGomul(models.Model):
	id = models.AutoField(primary_key=True)
	skst = models.CharField(max_length=42, blank=True, null=True, verbose_name='skammstöfun')
	nafn = models.CharField(max_length=85, blank=True, null=True, verbose_name='nafn')

	def __str__(self):
		return self.nafn

	class Meta:
		managed = False
		ordering = ('nafn',)
		db_table = 'baejatal_sveitarfelog_gomul'
		verbose_name = 'sveitarfélag (1970)'
		verbose_name_plural = 'sveitarfélög (1970)'


class BaejatalSveitarfelogNy(models.Model):
	id = models.AutoField(primary_key=True)
	skst = models.CharField(max_length=42, blank=True, null=True, verbose_name='skammstöfun')
	nafn = models.CharField(max_length=85, blank=True, null=True, verbose_name='nafn')

	def sveitarfelag(self):
		return self.id

	def __str__(self):
		return self.nafn

	class Meta:
		managed = False
		ordering = ('nafn', )
		db_table = 'baejatal_sveitarfelog_ny'
		verbose_name = 'sveitarfélag'
		verbose_name_plural = 'sveitarfélög'


class BaejatalSyslur(models.Model):
	id = models.AutoField(primary_key=True)
	skst = models.CharField(max_length=42, blank=True, null=True, verbose_name='skammstöfun')
	nafn = models.CharField(max_length=85, blank=True, null=True, verbose_name='nafn')

	def __str__(self):
		return self.nafn

	class Meta:
		managed = False
		#ordering = ('nafn',)
		db_table = 'baejatal_syslur'
		verbose_name = 'sýsla'
		verbose_name_plural = 'sýslur'


class BaejatalSveitarfelogGomulSyslur(models.Model):
	id = models.IntegerField(primary_key=True)
	sveitarfelag = models.ForeignKey('BaejatalSveitarfelogGomul', on_delete=models.DO_NOTHING, db_column='sveitarfelag')
	#hreppur = models.ForeignKey('BaejatalSveitarfelogGomul', on_delete=models.DO_NOTHING, db_column='sveitarfelag')
	sysla = models.ForeignKey('BaejatalSyslur', on_delete=models.DO_NOTHING, db_column='sysla')

	class Meta:
		managed = False
		db_table = 'baejatal_sveitarfelog_gomul_syslur'

	def __str__(self):
		return self.sveitarfelag.nafn


class BaejatalSveitarfelogNySyslur(models.Model):
	id = models.IntegerField(primary_key=True)
	sveitarfelag = models.ForeignKey('BaejatalSveitarfelogNy', on_delete=models.DO_NOTHING, db_column='sveitarfelag')
	sysla = models.ForeignKey(BaejatalSyslur, on_delete=models.DO_NOTHING, db_column='sysla')

	def __str__(self):
		return self.sveitarfelag.nafn

	def get_absolute_url(self):
		return reverse('sveitarfelag_detail', args=[str(self.id)])

	class Meta:
		managed = False
		db_table = 'baejatal_sveitarfelog_ny_syslur'


class BaejatalBaeirSveitarfelog(models.Model):
	baer = models.ForeignKey(BaejatalBaeir, on_delete=models.DO_NOTHING, db_column='baer')
	sveitarfelag = models.ForeignKey(BaejatalSveitarfelogNy, on_delete=models.DO_NOTHING, db_column='sveitarfelag')

	class Meta:
		managed = False
		db_table = 'baejatal_baeir_sveitarfelog_ny'


class BaejatalBaeirHreppar(models.Model):
	baer = models.ForeignKey(BaejatalBaeir, on_delete=models.DO_NOTHING, db_column='baer')
	hreppur = models.ForeignKey(BaejatalSveitarfelogGomul, on_delete=models.DO_NOTHING, db_column='sveitarfelag')

	class Meta:
		managed = False
		db_table = 'baejatal_baeir_sveitarfelog_gomul'


class Einstaklingar(models.Model):
	nafn = models.CharField(max_length=250, blank=True, null=True, verbose_name='nafn')
	aukanafn = models.CharField(max_length=250, blank=True, null=True, verbose_name='aukanafn')
	faedingarstadur = models.CharField(max_length=250, blank=True, null=True, verbose_name='fæðingarstaður')
	heimili = models.CharField(max_length=250, blank=True, null=True, verbose_name='heimili')
	faedingarar = models.IntegerField(blank=True, null=True, verbose_name='fæðingarár')
	danarar = models.IntegerField(blank=True, null=True, verbose_name='dánarár')

	stadir = models.ManyToManyField(
		'BaejatalBaeir',
		through='EinstaklingarBaeir',
		verbose_name = 'tengdir staðir'
	)

	class Meta:
		managed = False
		db_table = 'einstaklingar'
		verbose_name = 'einstaklingur'
		verbose_name_plural = 'einstaklingar'

	def __str__(self):
		return self.nafn

	def get_absolute_url(self):
		return reverse('einstaklingur_detail', args=[str(self.id)])


class EinstaklingarBaeir(models.Model):
	einstaklingur = models.ForeignKey(Einstaklingar, on_delete=models.DO_NOTHING, db_column='einstaklingur', verbose_name='einstaklingur')
	baer = models.ForeignKey(BaejatalBaeir, on_delete=models.DO_NOTHING, db_column='baer')
	tengsl = models.CharField(max_length=250, blank=True, null=True, verbose_name='tengsl', choices=[('heimili', 'Heimili'), ('fæðingarstaður', 'Fæðingarstaður')])
	upphafsar = models.IntegerField(blank=True, null=True, verbose_name='upphafsár')
	lokaar = models.IntegerField(blank=True, null=True, verbose_name='lokaár')

	class Meta:
		managed = False
		db_table = 'einstaklingar_baeir'
		verbose_name = 'tengdur staður'
		verbose_name_plural = 'tengdir staðir'


# Aukamódel fyrir view í gagnagruninum:
class Ornefnapakki(models.Model):
	id = models.IntegerField(primary_key=True)
	ornefni = models.CharField(max_length=250)
	samraemt = models.CharField(max_length=250)
	uuid = models.CharField(max_length=250)
	ornefnaskra = models.ForeignKey(Ornefnaskrar, on_delete=models.DO_NOTHING, db_column='ornefnaskra')
	baer = models.ForeignKey(BaejatalBaeir, on_delete=models.DO_NOTHING, db_column='baer')
	hreppur = models.ForeignKey(BaejatalSveitarfelogGomul, on_delete=models.DO_NOTHING, db_column='hreppur')
	sveitarfelag = models.ForeignKey(BaejatalSveitarfelogNy, on_delete=models.DO_NOTHING, db_column='sveitarfelag')
	sysla = models.ForeignKey(BaejatalSyslur, on_delete=models.DO_NOTHING, db_column='sysla')
	artal_skrar = models.IntegerField(blank=True, null=True, verbose_name='ártal skrár')

	def __str__(self):
		return self.ornefni

	class Meta:
		managed = False
		db_table = 'ornefnapakki'
		#ordering = ('ornefni',)


# Ábendingar notenda
class Abendingar(models.Model):
	nafn = models.CharField(max_length=250, blank=False, null=False, verbose_name='nafn sendanda')
	netfang = models.CharField(max_length=250, blank=False, null=False, verbose_name='netfang sendanda')
	simanumer = models.CharField(max_length=50, blank=True, null=True, verbose_name='símanúmer sendanda')
	skilabod = models.TextField(blank=True, null=True, verbose_name='skilaboð')
	entity_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='tegund gagns')
	entity_id = models.IntegerField(blank=True, null=True, verbose_name='auðkennisnúmer gagns')
	entity_name = models.TextField(blank=True, null=True, verbose_name='heiti gagns')
	inserttime = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='dagsetning')

	def entity_link(self):
		return mark_safe('<a href="https://nafnid.arnastofnun.is/%s/%s">%s</a>' % (self.entity_type, self.entity_id, self.entity_name))

	entity_link.short_description = 'Ábendingin varðar'
	entity_link.allow_tags = True

	def __str__(self):
		return self.nafn

	class Meta:
		managed = False
		db_table = 'abendingar'
		verbose_name = 'ábending notanda'
		verbose_name_plural = 'ábendingar notenda'

class Frumskraning(models.Model):
	fjoldi_skjala = models.IntegerField(blank=True, null=True, verbose_name='fjöldi skjala')
	athugasemd = models.TextField(blank=True, null=True, verbose_name='athugasemd')
	dagsetning_fra = models.CharField(max_length=100, blank=True, null=True, verbose_name='dagsetning frá', help_text='yyyy-mm-dd')
	dagsetning_til = models.CharField(max_length=100, blank=True, null=True, verbose_name='dagsetning til', help_text='yyyy-mm-dd')

	sveitarfelag_nuv = models.ForeignKey('BaejatalSveitarfelogNy', models.DO_NOTHING, blank=True, null=True, verbose_name='núverandi sveitarfélag')
	sveitarfelag_gamalt = models.ForeignKey('BaejatalSveitarfelogGomul', models.DO_NOTHING, blank=True, null=True, verbose_name='sveitarfélag (1970)')
	sysla = models.ForeignKey('BaejatalSyslur', models.DO_NOTHING, blank=True, null=True, verbose_name='sýsla')
	baer = models.ForeignKey('BaejatalBaeir', models.DO_NOTHING, blank=True, null=True, verbose_name='svæði')
	myndagogn = models.BooleanField(blank=False, null=False, default=False, verbose_name='myndagögn?')

	def __str__(self):
		return str(self.baer) if self.baer is not None else self.sveitarfelag_nuv.nafn if self.sveitarfelag_nuv is not None else self.sveitarfelag_gamalt.nafn if self.sveitarfelag_gamalt is not None else '-'

	class Meta:
		managed = False
		db_table = 'frumskraning'
		verbose_name = 'frumskráning'
		verbose_name_plural = 'frumskráningar'

class FrumskraningarBaeir(models.Model):
	baer = models.ForeignKey(BaejatalBaeir, on_delete=models.CASCADE, verbose_name='bær')
	frumskraning = models.ForeignKey(Frumskraning, on_delete=models.CASCADE, verbose_name='frumskráning')

	class Meta:
		managed = False
		db_table = 'frumskraningar_baer'
		verbose_name = 'tengdur bær/svæði'
		verbose_name_plural = 'aðrir tengir bæir/svæði'
