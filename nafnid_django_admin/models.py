# -*- coding: utf-8 -*-
from django.db import models
from django.utils.html import format_html

class Ornefnaskrar(models.Model):
	id = models.AutoField(primary_key=True)
	titill = models.CharField(max_length=300, blank=True, null=True)
	texti = models.TextField(blank=True, null=True)
	sysla = models.ForeignKey('BaejatalSyslur', models.DO_NOTHING, db_column='sysla', verbose_name='sýsla', blank=True, null=True)
	hreppur = models.ForeignKey('BaejatalSveitarfelogGomul', models.DO_NOTHING, db_column='hreppur', verbose_name='hreppur', blank=True, null=True)
	stafraent = models.BooleanField(blank=True, null=True, verbose_name='stafrænt?')
	pappir = models.BooleanField(blank=True, null=True, verbose_name='pappír?')
	pdf_skra_id = models.ForeignKey('PdfSkrarFinnur', models.DO_NOTHING, db_column='pdf_skra_id', verbose_name='pdf skrá', blank=True, null=True)
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
		verbose_name = 'Örnefni'
	)

	baeir = models.ManyToManyField(
		'BaejatalBaeir',
		through='OrnefnaskrarBaeir',
		verbose_name = 'bæir'
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


class OrnefnaskrarBaeir(models.Model):
	ornefnaskra = models.ForeignKey('Ornefnaskrar', models.DO_NOTHING, db_column='ornefnaskra', verbose_name='örnefnaskrá')
	baer = models.ForeignKey('BaejatalBaeir', models.DO_NOTHING, db_column='baer', verbose_name='bær')
	tegund = models.CharField(max_length=100, blank=True, null=True, verbose_name='tegund')

	class Meta:
		managed = False
		db_table = 'ornefnaskrar_baeir'
		verbose_name = 'bær'
		verbose_name_plural = 'bæir'


class OrnefnaskrarEinstaklingar(models.Model):
	einstaklingur = models.ForeignKey('Einstaklingar', models.DO_NOTHING, db_column='einstaklingur', verbose_name='einstaklingur')
	ornefnaskra = models.ForeignKey('Ornefnaskrar', models.DO_NOTHING, db_column='ornefnaskra', verbose_name='örnefnaskrá')
	hlutverk = models.CharField(max_length=200, blank=True, null=True, verbose_name='hlutverk', choices=[('skrasetjari', 'Skrásetjari'), ('heimildamadur', 'Heimildamaður'), ('starfsmaður örnefnastofnunar', 'Starfsmaður Örnefnastofnunar'), ('kortagerð', 'Kortagerð')])

	class Meta:
		managed = False
		db_table = 'ornefnaskrar_einstaklingar'
		verbose_name = 'einstaklingur'
		verbose_name_plural = 'einstaklingar'


class Ornefni(models.Model):
	ornefni = models.CharField(max_length=300, blank=True, null=True, verbose_name='örnefni')
	lat = models.FloatField(blank=True, null=True)
	lon = models.FloatField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'ornefni'
		verbose_name = 'örnefni'
		verbose_name_plural = 'örnefni'

	def __str__(self):
		return self.ornefni


class OrnefnaskrarOrnefni(models.Model):
	ornefni = models.ForeignKey(Ornefni, on_delete=models.DO_NOTHING, db_column='ornefni', verbose_name='örnefni')
	skra = models.ForeignKey(Ornefnaskrar, on_delete=models.DO_NOTHING, db_column='skra')

	class Meta:
		managed = False
		db_table = 'ornefnaskrar_ornefni'
		verbose_name = 'örnefni'
		verbose_name_plural = 'örnefni'


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

	def file_tag(self):
		#	<a href="http://nidhoggur.rhi.hi.is/nafnid-media/uploads/{0}">Slóð á skrá</a>
		map_html = """
			<embed src="http://nidhoggur.rhi.hi.is/nafnid-media/uploads/{0}" width="100%" height="800">
		"""

		return format_html(map_html,
			self.slod
		)

	file_tag.short_description = 'Pdf'
	file_tag.allow_tags = True

	def __str__(self):
		return self.slod.name

	class Meta:
		managed = False
		db_table = 'pdf_skrar_finnur'
		verbose_name = 'pdf skrá'
		verbose_name_plural = 'pdf skrár'


class BaejatalBaeir(models.Model):
	id = models.AutoField(primary_key=True)
	baejarnafn = models.CharField(max_length=85, blank=True, null=True, verbose_name='bæjarnafn')
	nuv_sveitarf = models.ForeignKey('BaejatalSveitarfelogNy', models.DO_NOTHING, db_column='nuv_sveitarf', verbose_name='núverandi sveitarfélag')
	gamalt_sveitarf = models.ForeignKey('BaejatalSveitarfelogGomul', models.DO_NOTHING, db_column='gamalt_sveitarf', verbose_name='sveitarfélag (1970)')
	sysla = models.ForeignKey('BaejatalSyslur', models.DO_NOTHING, db_column='sysla', verbose_name='sýsla')
	lbs_lykill = models.CharField(max_length=50, blank=True, null=True, verbose_name='lykill landsbókasafns')
	lat = models.FloatField(blank=True, null=True)
	lng = models.FloatField(blank=True, null=True)
	sveitarf_temp = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.baejarnafn+', '+str(self.nuv_sveitarf)+', '+str(self.sysla)

	class Meta:
		managed = False
		db_table = 'baejatal_baeir'
		verbose_name = 'bær'
		verbose_name_plural = 'bæir'


class BaejatalSveitarfelogGomul(models.Model):
	id = models.AutoField(primary_key=True)
	skst = models.CharField(max_length=42, blank=True, null=True, verbose_name='skammstöfun')
	nafn = models.CharField(max_length=85, blank=True, null=True, verbose_name='nafn')

	def __str__(self):
		return self.nafn

	class Meta:
		managed = False
		db_table = 'baejatal_sveitarfelog_gomul'
		verbose_name = 'sveitarfélag (1970)'
		verbose_name_plural = 'sveitarfélög (1970)'


class BaejatalSveitarfelogNy(models.Model):
	id = models.AutoField(primary_key=True)
	skst = models.CharField(max_length=42, blank=True, null=True, verbose_name='skammstöfun')
	nafn = models.CharField(max_length=85, blank=True, null=True, verbose_name='nafn')

	def __str__(self):
		return self.nafn

	class Meta:
		managed = False
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
		db_table = 'baejatal_syslur'
		verbose_name = 'sýsla'
		verbose_name_plural = 'sýslur'


class Einstaklingar(models.Model):
	nafn = models.CharField(max_length=250, blank=True, null=True, verbose_name='nafn')
	aukanafn = models.CharField(max_length=250, blank=True, null=True, verbose_name='aukanafn')
	faedingarstadur = models.CharField(max_length=250, blank=True, null=True, verbose_name='fæðingarstaður')
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

class EinstaklingarBaeir(models.Model):
	einstaklingur = models.ForeignKey(Einstaklingar, on_delete=models.DO_NOTHING, db_column='einstaklingur', verbose_name='einstaklingur')
	baer = models.ForeignKey(BaejatalBaeir, on_delete=models.DO_NOTHING, db_column='baer')
	tengsl = models.CharField(max_length=250, blank=True, null=True, verbose_name='tengsl', choices=[('heimili', 'Heimili'), ('fæðingarstaður', 'Fæðingarstaður')])

	class Meta:
		managed = False
		db_table = 'einstaklingar_baeir'
		verbose_name = 'tengdur staður'
		verbose_name_plural = 'tengdir staðir'