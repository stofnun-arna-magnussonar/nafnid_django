from django.contrib import admin

from .models import *

class SiteAdmin(admin.ModelAdmin):
	list_display = ['id', 'site_name']
	model = Site

class PageAdmin(admin.ModelAdmin):
	model = Page
	fields = [
		'title', 
		'url',
		('in_menu', 'menu_separator', 'use_as_link'),
		'content',
		'site'
	]
	list_display = ['title', 'url', 'in_menu', 'menu_separator', 'use_as_link', 'site', 'order']
	list_editable = ['url', 'in_menu', 'menu_separator', 'use_as_link', 'order']
	search_fields = ['title', 'url', 'content']
	list_filter = ['in_menu', 'menu_separator', 'use_as_link', 'site']
	list_display_links = ['title']



class ForsiduhlutarAdmin(admin.ModelAdmin):
	model = Forsiduhlutar
	fields = [
		'nafn', 
		'content',
		'css_class',
		'site'
	]
	list_filter = [ 'site']
	list_display = ['nafn','order', 'css_class']
	list_editable = ['order', 'css_class']
	search_fields = ['nafn']

admin.site.register(Page, PageAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Forsiduhlutar, ForsiduhlutarAdmin)
