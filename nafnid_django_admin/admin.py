from django.contrib import admin

from .models import *

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
		('stafraent', 'pappir')
	)
	inlines = [OrnefnaskrarTegundirInline, OrnefnaskrarOrnefniInline]

class TegundirAdmin(admin.ModelAdmin):
	pass

class OrnefniAdmin(admin.ModelAdmin):
	pass

admin.site.register(Ornefnaskrar, OrnefnaskrarAdmin)
admin.site.register(Ornefni, OrnefniAdmin)
admin.site.register(Tegundir, TegundirAdmin)
