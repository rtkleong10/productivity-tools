from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import UpdateView
from .models import UserProfile

@login_required
@require_http_methods(["GET"])
def logout_view(request):
	if request.method == 'GET':
		response = logout(request)
		return render(response, 'registration/logout.html')

@require_http_methods(["GET", "POST"])
def signup_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)

		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('web:home')

	else:
		form = UserCreationForm()

	return render(request, 'registration/signup.html', {'form': form})

class ProfileView(LoginRequiredMixin, UpdateView):
	model = UserProfile
	fields = (
		'timezone',
	)
	template_name = 'registration/profile.html'
	success_url = reverse_lazy('registration:profile')

	def get_object(self):
		user = self.request.user
		return user.profile