from django.db import models

class Ornefnaskrar(models.Model):
	titill = models.CharField(max_length=300, blank=True, null=True)
	texti = models.TextField(blank=True, null=True)
	sysla = models.CharField(max_length=20, blank=True, null=True, verbose_name='sýsla')
	hreppur = models.CharField(max_length=20, blank=True, null=True)
	heimildamadur = models.CharField(max_length=260, blank=True, null=True, verbose_name='heimildamaður')
	skrasetjari = models.CharField(max_length=260, blank=True, null=True, verbose_name='skrásetjari')
	dagsetning = models.DateField(blank=True, null=True)
	skra_id = models.CharField(max_length=260, blank=True, null=True)
	stada = models.CharField(max_length=300, blank=True, null=True, choices=[('Yfirfarið', 'Yfirfarið'), ('Í vinnslu', 'Í vinnslu')])
	stafraent = models.BooleanField(blank=True, null=True, verbose_name='stafrænt?')
	pappir = models.BooleanField(blank=True, null=True, verbose_name='pappír?')
	pdf_skra = models.ForeignKey('PdfSkrarFinnur', models.DO_NOTHING, db_column='pdf_skra', verbose_name='pdf skrá', blank=True, null=True)

	tegund = models.ManyToManyField(
		'Tegundir',
		through='OrnefnaskrarTegundir',
		verbose_name = 'Tegundir skráningar'
	)

	ornefni = models.ManyToManyField(
		'Ornefni',
		through='OrnefnaskrarOrnefni',
		verbose_name = 'Örnefni'
	)

	class Meta:
		managed = False
		db_table = 'ornefnaskrar'
		verbose_name = 'skjal'
		verbose_name_plural = 'skjöl'

	def __str__(self):
		return self.titill


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

class PdfSkrarFinnur(models.Model):
	slod = models.CharField(primary_key=True, max_length=500, blank=False, null=False, verbose_name='slóð')
	sysla_id = models.IntegerField(blank=True, null=True, verbose_name='auðkenni sýslu')
	hreppur_id = models.IntegerField(blank=True, null=True, verbose_name='auðkenni hrepps')
	sysla = models.CharField(max_length=300, blank=True, null=True, verbose_name='sýsla')
	hreppur = models.CharField(max_length=300, blank=True, null=True, verbose_name='hreppur')

	def __str__(self):
		return self.slod

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
		return self.skst

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
		return self.skst

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
		return self.skst

	class Meta:
		managed = False
		db_table = 'baejatal_syslur'
		verbose_name = 'sýsla'
		verbose_name_plural = 'sýslur'