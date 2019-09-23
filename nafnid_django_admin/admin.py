from django.contrib import admin

from .models import *

class PdfSkrarFinnurAdmin(admin.ModelAdmin):
	list_display = ('slod', 'sysla', 'hreppur')
	search_fields = ['slod', 'sysla', 'hreppur']
	list_filter = ['sysla', 'hreppur']


class OrnefnaskrarTegundirInline(admin.TabularInline):
	list_display = ('tegund')
	readonly_fields = ['id']
	model = Ornefnaskrar.tegund.through


class OrnefnaskrarOrnefniInline(admin.TabularInline):
	list_display = ('ornefni')
	readonly_fields = ['id']
	raw_id_field = ['ornefni']
	show_change_link = True
	model = Ornefnaskrar.ornefni.through


class OrnefnaskrarAdmin(admin.ModelAdmin):
	fields = (
		('titill', 'skra_id'),
		('sysla', 'hreppur'),
		'texti',
		('skrasetjari', 'heimildamadur'),
		'dagsetning',
		('stada', 'stafraent', 'pappir'),
		'pdf_skra'
	)
	inlines = [OrnefnaskrarTegundirInline, OrnefnaskrarOrnefniInline]
	raw_id_fields = ['pdf_skra']
	search_fields = ['tititt', 'skra_id', 'texti']
	list_filter = ['stada', 'stafraent', 'pappir']

class TegundirAdmin(admin.ModelAdmin):
	pass

class OrnefniAdmin(admin.ModelAdmin):
	pass

class BaejatalBaeirAdmin(admin.ModelAdmin):
	list_display = ['id', 'baejarnafn']
	list_filter = ['sysla', 'nuv_sveitarf', 'gamalt_sveitarf']

class BaejatalSveitarfelogGomulAdmin(admin.ModelAdmin):
	pass

class BaejatalSveitarfelogNyAdmin(admin.ModelAdmin):
	pass

class BaejatalSyslurAdmin(admin.ModelAdmin):
	pass

admin.site.register(Ornefnaskrar, OrnefnaskrarAdmin)
admin.site.register(Ornefni, OrnefniAdmin)
admin.site.register(Tegundir, TegundirAdmin)
admin.site.register(PdfSkrarFinnur, PdfSkrarFinnurAdmin)

admin.site.register(BaejatalBaeir, BaejatalBaeirAdmin)
admin.site.register(BaejatalSveitarfelogGomul, BaejatalSveitarfelogGomulAdmin)
admin.site.register(BaejatalSveitarfelogNy, BaejatalSveitarfelogNyAdmin)
admin.site.register(BaejatalSyslur, BaejatalSyslurAdmin)
