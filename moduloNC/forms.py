from django import forms
from django.forms import ModelForm
from .models import NC , AccionInm

class NCForm(ModelForm):

    class Meta:
        model = NC
        fields = ('titulo','descripcion','fechaSuceso','sector')

class AccionInmForm(ModelForm):

    class Meta:
        model = AccionInm
        fields = ('text',)