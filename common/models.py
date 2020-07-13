from django.db import models
from colorfield.fields import ColorField

class Color(models.Model):
	title = models.CharField(
		help_text='Name of the colour',
		max_length=200,
	)

	hex_code = ColorField(
		help_text='Name of the colour',
	)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ('id',)