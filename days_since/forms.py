from django import forms
from days_since.models import Activity

class ActivityForm(forms.ModelForm):
	class Meta:
		model = Activity
		# fields = ['pub_date', 'headline', 'content', 'reporter']