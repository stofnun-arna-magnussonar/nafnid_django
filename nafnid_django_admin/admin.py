from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter, DropdownFilter
from .models import *

class PdfSkrarFinnurAdmin(admin.ModelAdmin):
	def to_str(self, obj):
		return obj.__str__()

	fields = (
		'sysla_id',
		'hreppur_id',
		'bt_hreppur',
		'bt_sysla',
		'sysla',
		'hreppur',
		'slod',
		'file_tag'
	)
	readonly_fields = ['file_tag']
	list_display = ('to_str', 'sysla', 'hreppur')
	search_fields = ['slod', 'sysla', 'hreppur']
	list_filter = (
		('bt_sysla', RelatedDropdownFilter),
		('bt_hreppur', RelatedDropdownFilter),
		('sysla', DropdownFilter),
		('hreppur', DropdownFilter),
	)

class OrnefnaskrarTegundirInline(admin.TabularInline):
	list_display = ('tegund')
	readonly_fields = ['id']
	model = Ornefnaskrar.tegund.through


class OrnefnaskrarStadaInline(admin.TabularInline):
	list_display = ('stada', 'athugasemd')
	readonly_fields = ['id']
	model = Ornefnaskrar.stada.through


class OrnefnaskrarOrnefniInline(admin.TabularInline):
	list_display = ('ornefni')
	readonly_fields = ['id']
	raw_id_fields = ['ornefni']
	show_change_link = True
	model = Ornefnaskrar.ornefni.through


class BaeirOrnefniInline(admin.TabularInline):
	list_display = ('baer')
	readonly_fields = ['id']
	raw_id_fields = ['baer']
	show_change_link = True
	model = Ornefnaskrar.baeir.through


class OrnefnaskrarEinstaklingarInline(admin.TabularInline):
	list_display = ('einstaklingur')
	raw_id_fields = ['einstaklingur']
	show_change_link = True
	model = Ornefnaskrar.einstaklingar.through


class OrnefnaskrarAdmin(admin.ModelAdmin):
	fields = (
		('titill', 'id'),
		('sysla', 'hreppur'),
		'texti',
		'stafraent', 
		'pappir',
		'pdf_skra_id'
	)
	inlines = [
		OrnefnaskrarTegundirInline, 
		OrnefnaskrarStadaInline, 
		BaeirOrnefniInline,
		OrnefnaskrarEinstaklingarInline,
		OrnefnaskrarOrnefniInline
	]
	readonly_fields = ['id']
	raw_id_fields = ['pdf_skra_id']
	search_fields = ['titill', 'texti']
	list_filter = (
		'stada', 
		'stafraent', 
		'pappir', 
		('sysla', RelatedDropdownFilter),
		('hreppur', RelatedDropdownFilter)
	)

class TegundirAdmin(admin.ModelAdmin):
	pass

class StadaAdmin(admin.ModelAdmin):
	pass

class OrnefniAdmin(admin.ModelAdmin):
	pass

class BaejatalBaeirAdmin(admin.ModelAdmin):
	list_display = ['id', 'baejarnafn', 'nuv_sveitarf', 'gamalt_sveitarf', 'sysla', 'lbs_lykill']
	list_filter = ['sysla', 'nuv_sveitarf', 'gamalt_sveitarf']
	search_fields = ['baejarnafn', 'sysla__nafn', 'nuv_sveitarf__nafn', 'gamalt_sveitarf__nafn']

class EinstaklingarAdmin(admin.ModelAdmin):
	list_display = ['id', 'nafn', 'aukanafn','faedingarstadur','faedingarar']
	list_editable = ['nafn', 'nafn', 'aukanafn','faedingarstadur','faedingarar']
	search_fields = ['nafn']

class BaejatalSveitarfelogGomulAdmin(admin.ModelAdmin):
	pass

class BaejatalSveitarfelogNyAdmin(admin.ModelAdmin):
	pass

class BaejatalSyslurAdmin(admin.ModelAdmin):
	pass

admin.site.register(Ornefnaskrar, OrnefnaskrarAdmin)
admin.site.register(Ornefni, OrnefniAdmin)
admin.site.register(Tegundir, TegundirAdmin)
admin.site.register(Stada, StadaAdmin)
admin.site.register(PdfSkrarFinnur, PdfSkrarFinnurAdmin)
admin.site.register(Einstaklingar, EinstaklingarAdmin)

admin.site.register(BaejatalBaeir, BaejatalBaeirAdmin)
admin.site.register(BaejatalSveitarfelogGomul, BaejatalSveitarfelogGomulAdmin)
admin.site.register(BaejatalSveitarfelogNy, BaejatalSveitarfelogNyAdmin)
admin.site.register(BaejatalSyslur, BaejatalSyslurAdmin)
