from django import forms
from api.models import Activity

class ActivityForm(forms.ModelForm):
	class Meta:
		model = Activity
		# fields = ['pub_date', 'headline', 'content', 'reporter']