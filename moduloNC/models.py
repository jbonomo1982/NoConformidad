from django.db import models
from django.utils import timezone


class Sector(models.Model):

    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10 ,help_text="Abreviatura del sector.")
    nombre = models.CharField(max_length=100)

    def __str__(self):
        d = "Sector " + self.codigo
        return d


class NC(models.Model):

    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    codigo = models.CharField(max_length=200 ,help_text="Código propio del sistema.",blank=True,null=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fechaApertura = models.DateTimeField(
            default=timezone.now)
    fechaSuceso = models.DateTimeField(
            blank=True, null=True ,help_text="Ingresar dd/mm/aaaa hh:mm:ss")
    sector= models.ForeignKey(Sector, default=None, on_delete=models.CASCADE)

    cerrada = models.BooleanField(default=False,help_text="Indica si la NC está cerrada.")


    def __str__(self):
        return '{0} {1}'.format(self.titulo,self.codigo)

class Contribuyente(models.Model):
    contribuyente = models.ManyToManyField('auth.User')
    nc = models.OneToOneField(NC, on_delete=models.CASCADE)
    def __str__(self):
        return 'Contribuyentes de {0}'.format(self.nc)





class CierreNC(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    nc = models.ForeignKey(NC, on_delete=models.CASCADE)
    fechaCierre = models.DateTimeField(
            default=timezone.now)
    observacion = models.TextField(help_text=
    "Informar sobre algo especial en el cierre de NC")
    aceptado = models.BooleanField(default=False,help_text="Indica si el cierre de nc está aceptado.")

    def __str__(self):
        return 'Cierre de NC: {0}: {1}--ESTADO: {2}'.format(self.nc,self.pk,self.aceptado)
        

class AnalisisCausa(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    nc = models.ForeignKey(NC, on_delete=models.CASCADE)
    fecha = models.DateTimeField(
        default=timezone.now)
    descr = models.TextField(help_text="Acá se describe el análisis de causa de la  NC")
    publicado = models.BooleanField(default=False,help_text="Indica si la entrada está aceptada.")

    def __str__(self):
        return 'Analisis causa: {0} {1}'.format(self.autor,self.nc)



class AccionInm(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    nc = models.ForeignKey(NC, on_delete=models.CASCADE)
    created_date = models.DateTimeField(
            default=timezone.now)
    text = models.TextField(help_text=
    "Describir cómo se trato corregir la acción que genera la NC, en una prímera instancia")
    publicado = models.BooleanField(default=False,help_text="Indica si la entrada está aceptada.")
    fecha_publicado = models.DateTimeField(blank=True,null=True)
    def despublicar(self):
        self.publicado = False


    def __str__(self):
        return 'Acción Inm: {0} {1}'.format(self.autor,self.nc)

class AccionCorrectiva(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    nc = models.ForeignKey(NC, on_delete=models.CASCADE)
    created_date = models.DateTimeField(
            default=timezone.now)
    text = models.TextField(help_text=
    "Describir cómo se piensa corregir la acción que genera la NC,")
    publicado = models.BooleanField(default=False,help_text="Indica si la entrada está aceptada.")
    fechalimite= models.DateTimeField(help_text="Ingresar la fecha en la cual debe estar implementada la AC \n con el siguiente formato: dd/mm/aaaa hh:mm:ss")

    def __str__(self):
        return 'Acción Correctiva: {0} {1}'.format(self.autor,self.nc)

class VerificaAC(models.Model):
    encargado = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    nc = models.ForeignKey(NC, on_delete=models.CASCADE)
    ac = models.ForeignKey(AccionCorrectiva, on_delete=models.CASCADE)
    created_date = models.DateTimeField(
            default=timezone.now)
    publicado = models.BooleanField(default=False,help_text="Indica si la entrada está aceptada.")
    fechaVerif= models.DateTimeField()
    resultado=models.TextField()
    metodoVerif= models.TextField()

    def __str__(self):
        return 'Verificacion de NC: {0}, AC: {1}'.format(self.nc,self.ac)

class Archivo(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=None)
    nc = models.ForeignKey(NC, on_delete=models.CASCADE,default=None)
    created_date = models.DateTimeField(
            default=timezone.now)
    document = models.FileField(upload_to='documentos/')
    descr = models.TextField(help_text=
    "Describir el archivo que se sube.")
    publicado = models.BooleanField(default=False,help_text="Indica si la entrada está aceptada.")

    def __str__(self):
        return 'Archivo Adjunto de NC: {0}: {1}'.format(self.nc,self.pk)



