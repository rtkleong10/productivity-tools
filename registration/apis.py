from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from .models import UserProfile

class ProfileView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = ProfileSerializer

	def get_object(self):
		user = self.request.user
		return UserProfile.objects.get(user=user)
