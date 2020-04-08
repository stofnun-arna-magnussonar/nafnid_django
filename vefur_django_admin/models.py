from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Site(models.Model):
	id = models.AutoField(primary_key=True, db_column='id')
	site_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='heiti')

	def __str__(self):
		return self.site_name

	class Meta:
		managed = False
		db_table = 'vefur_pages_sites'
		verbose_name = 'Síðuhluti'
		verbose_name_plural = 'Síðuhlutar'

class Page(models.Model):
	id = models.AutoField(primary_key=True, db_column='id')
	title = models.CharField(max_length=200, null=False, blank=False, default='', verbose_name='titill')
	url = models.CharField(max_length=100, null=False, blank=False, default='', verbose_name='slóð')
	content = RichTextUploadingField(null=True, blank=True, verbose_name='innihald')
	in_menu = models.BooleanField(default=False, verbose_name='birta í valmynd')
	menu_separator = models.BooleanField(default=False, verbose_name='skipting valmyndar')
	use_as_link = models.BooleanField(default=False, verbose_name='tengill')
	order = models.IntegerField(default=0, blank=True, verbose_name='röðun')
	site = models.ForeignKey(Site, on_delete=models.DO_NOTHING, db_column='site', default=1, verbose_name='síðuhluti')

	def __str__(self):
		return self.title

	class Meta():
		managed = False
		verbose_name = 'síða'
		verbose_name_plural = 'síður'
		db_table = 'vefur_pages'
		ordering = ['order']

class Forsiduhlutar(models.Model):
	nafn = models.CharField(max_length=250, blank=True, null=True, verbose_name='nafn')
	content = RichTextUploadingField(blank=True, null=True, verbose_name='innihald')
	order = models.IntegerField(blank=True, null=True, verbose_name='röðun')
	css_class = models.CharField(max_length=250, blank=True, null=True, verbose_name='css klassi')
	site = models.ForeignKey(Site, on_delete=models.DO_NOTHING, db_column='site', default=1, verbose_name='síðuhluti')

	class Meta:
		managed = False
		db_table = 'vefur_forsiduhlutar'
		verbose_name = 'forsíðuhlutar'
		verbose_name_plural = 'forsíðuhluti'
		ordering = ['order']

