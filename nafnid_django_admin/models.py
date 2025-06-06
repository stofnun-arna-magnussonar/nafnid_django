# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


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
		verbose_name='Örnefni',
		related_name='ornefnaskrar_ornefni'
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
	baer = models.ForeignKey('BaejatalBaeir', models.DO_NOTHING, db_column='baer', verbose_name='svæði')
	tegund = models.CharField(max_length=100, blank=True, null=True, verbose_name='tegund')

	class Meta:
		managed = False
		db_table = 'ornefnaskrar_baeir'
		verbose_name = 'svæði'
		verbose_name_plural = 'svæði'


class BaeirOrnefnaskrar(models.Model):
	ornefnaskra = models.ForeignKey('Ornefnaskrar', models.DO_NOTHING, db_column='ornefnaskra', verbose_name='örnefnaskrá')
	baer = models.ForeignKey('BaejatalBaeir', models.DO_NOTHING, db_column='baer', verbose_name='svæði')
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
	hlutverk = models.ForeignKey('Hlutverk', models.DO_NOTHING, db_column='hlutv', blank=True, null=True)

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
		try:
			return self.hlutverk.hlutverk
		except:
			return '-'


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

	ornefnaskrar = models.ManyToManyField(
		'Ornefnaskrar',
		through='OrnefnaskrarOrnefni',
		verbose_name='Örnefnaskrár',
		related_name='ornefni_ornefnaskrar'
	)


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
	skra_texti = models.TextField()

	class Meta:
		managed = False
		db_table = 'ornefnaskrar_ocrornefni'
		verbose_name = 'örnefni'
		verbose_name_plural = 'örnefni'

class OrnefnaskrarOrnefnapakki(models.Model):
	ornefni = models.ForeignKey('Ornefnapakki', on_delete=models.DO_NOTHING, db_column='ocrornefni', related_name='ornefnaskrar')
	ornefnaskra = models.ForeignKey(Ornefnaskrar, on_delete=models.DO_NOTHING, db_column='skra')
	skra_texti = models.TextField()

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
	sveitarfelag = models.ForeignKey('BaejatalSveitarfelogNy', models.DO_NOTHING, db_column='nuv_sveitarf', verbose_name='núverandi sveitarfélag', blank=True, null=True)
	hreppur = models.ForeignKey('BaejatalSveitarfelogGomul', models.DO_NOTHING, db_column='gamalt_sveitarf', verbose_name='sveitarfélag (1970)', blank=True, null=True)
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

	def map_tag(self):
		map_html = """
			<link rel="stylesheet" href="https://unpkg.com/leaflet@1.2.0/dist/leaflet.css" />
			<script src="https://unpkg.com/leaflet@1.2.0/dist/leaflet.js"></script>
			<div id="admin_place_map" style="width: 100%; height: 600px;"></div>
			<div class="form-row field-url">
				<div>
					<label for="geocode_input">Leita að heimilsfangi:</label>
					<input type="text" class="vTextField" maxlength="300" id="geocode_input" value="">
				</div>
				<div id="geocode_results" style="margin-top: 10px"></div>
			</div>
			<script type="text/javascript">
				var updateLatLng = function(lat, lng) {{
					if (!django_isf_marker) {{
						django_isf_marker = L.marker([lat, lng]); // Lägger till en L.marker
						django_isf_marker.addTo(django_isf_map);
					}}
					django_isf_marker.setLatLng([lat, lng]);
					django.jQuery('#id_lat').val(parseFloat(lat).toFixed(6)); // Skriver e.latlng.lat från punkter var man klickade på kartan till "lat" fältet
					django.jQuery('#id_lng').val(parseFloat(lng).toFixed(6)); // Skriver e.latlng.lng från punkter var man klickade på kartan till "lng" fältet
				}};
				var django_isf_map = L.map("admin_place_map").setView([({0} > 0 ? {0} : 64.963051), ({1} > 0 ? {1} : -19.020836)], 6); // Skapar en karta
				L.tileLayer("http://{{s}}.tile.osm.org/{{z}}/{{x}}/{{y}}.png", {{attribution: "&copy; <a href='http://osm.org/copyright'>OpenStreetMap</a> contributors"}}).addTo(django_isf_map);
				var django_isf_marker;
				if ({0} != 0 && {1} != 0) {{
					django_isf_marker = L.marker([{0}, {1}]); // Lägger till en L.marker
					django_isf_marker.addTo(django_isf_map);
					django_isf_map.setView(django_isf_marker.getLatLng());
				}}
				django_isf_map.on('click', function(e) {{ // Map click handler
					updateLatLng(e.latlng.lat, e.latlng.lng);
				}});
				setTimeout(function() {{
					django_isf_map.invalidateSize();
				}}, 200);
				django.jQuery('#geocode_input').keypress(function(event) {{
					if (event.keyCode == 13) {{
						event.preventDefault();
						django.jQuery.getJSON('https://nominatim.openstreetmap.org/search?q='+django.jQuery('#geocode_input').val()+'&format=json', function(data) {{
							django.jQuery('#geocode_results').html('');

							if (data && data.length > 0) {{
								data.forEach(function(item) {{
									var listItem = django.jQuery('<a/>', {{
										text: item.display_name,
										style: 'display: block; margin-bottom: 5px;',
										href: '#'
									}});

									listItem.click(function(event) {{
										event.preventDefault();

										updateLatLng(item.lat, item.lon);
										django_isf_map.setView([item.lat, item.lon], 6);
									}})
									django.jQuery('#geocode_results').append(listItem);
								}});
							}}
						}});
					}}
				}});
			</script>
		"""



		lat = str(self.lat) if self.lat is not None else '0'
		lng = str(self.lng) if self.lat is not None else '0'

		formatted = map_html.format(lat, lng)

		return mark_safe(formatted)
		#return mark_safe(map_html % lat, lat, lng, lng, lat, lng, lat, lng)

	map_tag.short_description = 'Kort'
	map_tag.allow_tags = True

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
	#ornefnaskrar = models.ManyToManyField(OrnefnaskrarOrnefnapakki, related_name='ornefnaskrar')
	#ornefnaskrar = models.ManyToManyField(Ornefnaskrar, through=OrnefnaskrarOrnefnapakki, related_name='ornefnaskrar')

	def __str__(self):
		return self.ornefni

	class Meta:
		managed = False
		db_table = 'mv_ornefnapakki'
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
	afgreitt = models.BooleanField(verbose_name='afgreitt')

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
	baer = models.ForeignKey(BaejatalBaeir, on_delete=models.CASCADE, verbose_name='svæði')
	frumskraning = models.ForeignKey(Frumskraning, on_delete=models.CASCADE, verbose_name='frumskráning')

	class Meta:
		managed = False
		db_table = 'frumskraningar_baer'
		verbose_name = 'tengdur bær/svæði'
		verbose_name_plural = 'aðrir tengir bæir/svæði'

class Geoleit(models.Model):
	type = models.TextField(blank=True, null=True)
	name = models.CharField(max_length=255, blank=True, null=True)
	baer_id = models.IntegerField(blank=True, null=True)
	baer_name = models.CharField(max_length=255, blank=True, null=True)
	ornefnaskra = models.IntegerField(blank=True, null=True)
	hreppur_id = models.IntegerField(blank=True, null=True)
	hreppur = models.CharField(max_length=255, blank=True, null=True)
	sysla_id = models.IntegerField(blank=True, null=True)
	sysla = models.CharField(max_length=255, blank=True, null=True)
	tegund = models.CharField(max_length=255, blank=True, null=True)
	tegund_id = models.IntegerField(blank=True, null=True)
	lat = models.FloatField(blank=True, null=True)
	lng = models.FloatField(blank=True, null=True)
	article_count = models.IntegerField(blank=True, null=True)

	class Meta:
		managed = False  # Created from a view. Don't remove.
		db_table = 'geoleit'


class Grunngogn(models.Model):
	frumskraning = models.ForeignKey('Frumskraning', models.CASCADE, blank=True, null=True, verbose_name='frumskráning')

	sveitarfelag_nuv = models.ForeignKey('BaejatalSveitarfelogNy', models.DO_NOTHING, blank=True, null=True, verbose_name='núverandi sveitarfélag')
	sveitarfelag_gamalt = models.ForeignKey('BaejatalSveitarfelogGomul', models.DO_NOTHING, blank=True, null=True, verbose_name='sveitarfélag (1970)')
	sysla = models.ForeignKey('BaejatalSyslur', models.DO_NOTHING, blank=True, null=True, verbose_name='sýsla')
	baer = models.ForeignKey('BaejatalBaeir', models.DO_NOTHING, blank=True, null=True, verbose_name='svæði')

	athugasemd = models.TextField(blank=True, null=True)
	dagsetning_fra = models.CharField(max_length=100, blank=True, null=True)
	dagsetning_til = models.CharField(max_length=100, blank=True, null=True)
	myndagogn = models.BooleanField(blank=False, null=False, default=False, verbose_name='myndagögn?')

	class Meta:
		managed = False
		db_table = 'grunngogn'

	def __str__(self):
		return str(self.baer) if self.baer is not None else self.sveitarfelag_nuv.nafn if self.sveitarfelag_nuv is not None else self.sveitarfelag_gamalt.nafn if self.sveitarfelag_gamalt is not None else '-'

class GrunngognBaer(models.Model):
	grunngogn = models.ForeignKey('Grunngogn', models.CASCADE, blank=True, null=True, verbose_name='grunngagn')
	baer = models.ForeignKey('BaejatalBaeir', models.CASCADE, blank=True, null=True, verbose_name='svæði')

	class Meta:
		managed = False
		db_table = 'grunngogn_baer'


class ArticleCollections(models.Model):
	name = models.CharField(max_length=255, blank=True, null=True)
	description = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		managed = False
		db_table = 'article_collections'
		verbose_name = 'greinasafn'
		verbose_name_plural = 'greinasöfn'


class Articles(models.Model):
	title = models.CharField(max_length=255, blank=True, null=True, verbose_name='titill')
	content = RichTextUploadingField(null=True, blank=True, verbose_name='innihald')
	article_collection = models.ForeignKey(ArticleCollections, models.SET_NULL, blank=True, null=True, verbose_name='greinasafn')
	authors = models.ManyToManyField(Einstaklingar, through='ArticlesAuthors', verbose_name='höfundar')
	baeir = models.ManyToManyField(BaejatalBaeir, through='ArticlesBaeir', verbose_name='tengdir bæir')

	def __str__(self):
		return self.title

	class Meta:
		managed = False
		db_table = 'articles'
		verbose_name = 'grein'
		verbose_name_plural = 'greinar'
		ordering = ['title']


class ArticlesAuthors(models.Model):
	article = models.ForeignKey(Articles, models.CASCADE, blank=True, null=True, related_name='article_author', verbose_name='grein')
	einstaklingar = models.ForeignKey(Einstaklingar, models.CASCADE, blank=True, null=True, verbose_name='höfundur')

	class Meta:
		managed = False
		db_table = 'articles_authors'
		verbose_name = 'höfundur greinar'
		verbose_name_plural = 'höfundar greina'


class ArticlesBaeir(models.Model):
	article = models.ForeignKey(Articles, models.CASCADE, blank=True, null=True, verbose_name='grein')
	baeir = models.ForeignKey(BaejatalBaeir, models.CASCADE, blank=True, null=True, related_name='greinar', verbose_name='bær')

	class Meta:
		managed = False
		db_table = 'articles_baeir'
		verbose_name = 'tengdur bær'
		verbose_name_plural = 'tengdir bæir'

class NofnIslendingaGreinar(models.Model):
	texti = models.TextField(verbose_name='texti')
	heimild = models.TextField(null=True, blank=True)
	ath1 = models.TextField(null=True, blank=True)
	ath2 = models.TextField(null=True, blank=True)
	#nafn = models.CharField(max_length=255, verbose_name='uppflettinafn')
	#visun = models.CharField(max_length=255, verbose_name='vísun', null=True, blank=True)
	visun = models.ForeignKey('NofnIslendingaNofn', models.SET_NULL, verbose_name='vísun', null=True, blank=True, related_name='visun')

	#sja = models.CharField(max_length=255, verbose_name='vísun', null=True, blank=True)
	sja = models.ForeignKey('NofnIslendingaNofn', models.SET_NULL, verbose_name='sjá', null=True, blank=True, related_name='sja')

	def __str__(self):
		return str(NofnIslendingaNofn.objects.filter(grein__id=self.id).first())

	class Meta:
		managed = False
		db_table = 'nofn_islendinga_greinar'
		verbose_name = 'Nöfn íslendinga: greina'
		verbose_name_plural = 'Nöfn íslendinga: greinar'
		ordering = ['nafn__id']


class NofnIslendingaNofn(models.Model):
	nafn = models.CharField(max_length=255, verbose_name='uppflettinafn')
	ofl = models.CharField(max_length=20, blank=True, null=True, verbose_name='kyn')
	beyging = models.CharField(max_length=255, blank=True, null=True, verbose_name='beying')
	#grein = models.CharField(max_length=255, blank=True, null=True, verbose_name='beying')
	grein = models.ForeignKey(NofnIslendingaGreinar, models.CASCADE, related_name='nafn')
	rnum = models.IntegerField(verbose_name='raðnúmer', null=True, blank=True)
	adalord = models.BooleanField(verbose_name='aðalnafn')
	rownum = models.IntegerField()

	def __str__(self):
		return self.nafn

	class Meta:
		managed = False
		db_table = 'nofn_islendinga_uppflettiord'
		verbose_name = 'Nöfn íslendinga'
		verbose_name_plural = 'Nöfn íslendinga'
		ordering = ['id']
