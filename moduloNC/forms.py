from django import forms
from django.forms import ModelForm
from .models import NC , AccionInm, AnalisisCausa

class NCForm(ModelForm):

    class Meta:
        model = NC
        fields = ('titulo','descripcion','fechaSuceso','sector')

class AccionInmForm(ModelForm):

    class Meta:
        model = AccionInm
        fields = ('text',)

class AccionInmFormEditor(ModelForm):

    class Meta:
        model = AccionInm
        fields = ('publicado',)


class AnalisisForm(ModelForm):

    class Meta:
        model = AnalisisCausa
        fields = ('descr',)

class AnalisisFormEditor(ModelForm):

    class Meta:
        model = AnalisisCausa
        fields = ('publicado',)