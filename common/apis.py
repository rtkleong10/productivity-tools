import pytz
from rest_framework import views, generics
from rest_framework.response import Response
from common.serializers import ColorSerializer
from common.models import Color

class ColorView(generics.ListAPIView):
	queryset = Color.objects.order_by("id")
	serializer_class = ColorSerializer

class TimezoneView(views.APIView):
	def get(self, request):
		return Response(pytz.all_timezones)
