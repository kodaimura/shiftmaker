"""
from django import forms
from .models import Shift

class Shift(forms.ModelForm):
	class Meta:
		model = Shift
		fields = ('shift', 'candidate') 
"""