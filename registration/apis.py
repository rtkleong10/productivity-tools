from django.contrib.auth import logout, login
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import ProfileSerializer
from .models import UserProfile

class ProfileView(generics.RetrieveUpdateAPIView):
	"""
	Lists the user settings
	"""
	permission_classes = [IsAuthenticated]
	serializer_class = ProfileSerializer

	def get_object(self):
		user = self.request.user
		return UserProfile.objects.get(user=user)

class LoginView(APIView):
	"""
	Allows you to login for session login. If you want to obtain the JWT, you need to use jwt/create.
	"""
	serializer_class = AuthTokenSerializer

	def post(self, request):
		serializer = self.serializer_class(
			data=request.data,
			context={'request': request}
		)
		serializer.is_valid(raise_exception=True)

		user = serializer.validated_data['user']
		login(request, user)

		return Response({
			"detail": "Welcome to the Productivity Tools API, {}.".format(user.username)
		})

class LogoutView(APIView):
	"""
	Allows you to logout from the session. You need to perform a POST request (can leave the body empty).
	"""
	permission_classes = [IsAuthenticated]

	def post(self, request):
		logout(request)
		return Response({
			"detail": "You have logged out."
		})
