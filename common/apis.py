import pytz
from collections import OrderedDict
from django.urls import NoReverseMatch
from rest_framework.reverse import reverse
from rest_framework import views, generics
from rest_framework.response import Response
from common.serializers import ColorSerializer
from common.models import Color

class ColorListView(generics.ListAPIView):
	"""
	List of all the colors
	"""
	queryset = Color.objects.order_by("id")
	serializer_class = ColorSerializer

class TimezoneListView(views.APIView):
	"""
	List of all the possible timezones
	"""
	def get(self, request):
		return Response(pytz.all_timezones)

class HomeView(views.APIView):
	ROOT_URLS = {
		"API Root": "common:api-root",
		"Auth Root": "registration:api-root",
		"Admin Portal": "admin:index",
	}

	def get(self, request, *args, **kwargs):
		ret = OrderedDict()

		for key, url_name in HomeView.ROOT_URLS.items():
			try:
				ret[key] = reverse(
					url_name,
					args=args,
					kwargs=kwargs,
					request=request,
					format=kwargs.get('format', None)
				)
			except NoReverseMatch:
				continue

		return Response(ret)
