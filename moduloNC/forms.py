from django import forms
from django.forms import ModelForm
from .models import NC , AccionInm, AnalisisCausa, AccionCorrectiva, VerificaAC, Archivo, CierreNC

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

class AccionCorrectivaForm(ModelForm):

    class Meta:
        model = AccionCorrectiva
        fields = ('text','fechalimite',)

class AccionCorrectivaFormEditor(ModelForm):

    class Meta:
        model = AccionCorrectiva
        fields = ('publicado',)

class VerificaACForm(ModelForm):

    class Meta:
        model = VerificaAC
        fields = ('encargado','fechaVerif', 'resultado','metodoVerif',)

class VerificaACFormEditor(ModelForm):

    class Meta:
        model = VerificaAC
        fields = ('publicado',)

class ArchivoForm(ModelForm):

    class Meta:
        model = Archivo
        fields = ('document','descr',)

class ArchivoFormEditor(ModelForm):

    class Meta:
        model = Archivo
        fields = ('publicado',)

class CierreNCForm(ModelForm):

    class Meta:
        model = CierreNC
        fields = ('observacion',)

class CierreNCFormEditor(ModelForm):

    class Meta:
        model = CierreNC
        fields = ('aceptado',)