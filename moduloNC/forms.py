from django import forms
from django.forms import ModelForm
from .models import NC

class NCForm(ModelForm):

    class Meta:
        model = NC
        fields = ('titulo','descripcion','fechaSuceso','sector')