from .models import *
from rest_framework import serializers


class PageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Page
		fields = ('url',
			'title',
			'menu_separator'
		)


class ForsiduhlutarSerializer(serializers.ModelSerializer):
	class Meta:
		model = Forsiduhlutar
		fields = ('content',
			'css_class',
			'order'
		)

class SinglePageSerializer(serializers.ModelSerializer):
	path = serializers.SerializerMethodField()

	def get_path(self, obj):
		def get_path_object(path):

			return {
				'path': path
			}

		path_list = list(filter(None, obj.url.split('/')))
		last_path = path_list

		return_list = []

		i = 0
		while i < len(path_list)-1:
			last_path = last_path[:-1]

			path_url = '/'+'/'.join(last_path)+'/'

			path_model = Page.objects.filter(url=path_url)

			return_list.append({
				'path': path_url,
				'title': path_model[0].title
			})

			i += 1

		return_list.reverse()

		return_list.append({
			'path': obj.url,
			'title': obj.title
		})


		return return_list

	class Meta:
		model = Page
		fields = ('id',
			'url',
			'title',
			'content',
			'path'
		)

