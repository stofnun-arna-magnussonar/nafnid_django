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
	stafraent = models.BooleanField(blank=True, null=True, verbose_name='stafrænt?')
	pappir = models.BooleanField(blank=True, null=True, verbose_name='pappír?')

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
		verbose_name = 'örnefnaskrá'
		verbose_name_plural = 'örnefnaskrár'

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
		verbose_name = 'tegund örnefnaskrár'
		verbose_name_plural = 'tegund örnefnaskrár'
