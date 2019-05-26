# Create your views here.

from django.shortcuts import render
from .models import NC, AccionInm, Contribuyente, AnalisisCausa,AccionCorrectiva, VerificaAC, Archivo
from django.views import generic
from .forms import NCForm, AccionInmForm, AccionInmFormEditor, AnalisisForm, AnalisisFormEditor, AccionCorrectivaForm, AccionCorrectivaFormEditor, VerificaACForm, VerificaACFormEditor, ArchivoForm, ArchivoFormEditor
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone

# Create your views here.

def index(request):
    nc = NC.objects.all().count()
    nc_fin = NC.objects.filter(cerrada = True).count()
    return render(request, 'moduloNC/index.html', {'nc':nc,'nc_fin': nc_fin})

class NCListView(generic.ListView):
    model = NC

class NCDetailView(generic.DetailView):
    model = NC

def nc_new(request):
    if request.method == "POST":
        form = NCForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            c = Contribuyente(nc=NC.objects.get(pk = post.pk))
            c.save()
            return redirect('nc-detail', pk=post.pk)
    else:
        form = NCForm()
    return render(request, 'moduloNC/nueva_nc.html', {'form': form})

def AccionInm_new(request,pk):
    nc = NC.objects.get(pk=pk)
    if request.method == "POST":
        form = AccionInmForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            if nc.autor != post.autor:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()
                    
            post.nc = nc
            post.save()
            return redirect('AnalisisCausa-detail', pk=post.pk)
    else:
        
        form = AccionInmForm()
    return render(request, 'moduloNC/nuevaAnalisis.html', {'form': form,'nc':nc})

def AccionInm_edit(request, pk):
    #Editar en realidad tiene que ser crear una nueva instancia sobre otra anterior
    post = get_object_or_404(AccionInm, pk=pk)
    nc = post.nc
    if request.method == "POST":
        form = AccionInmForm(request.POST)
        
        if form.is_valid():
            b= form.save(commit=False)
            b.autor = request.user
            b.nc = nc

            if nc.autor != request.user:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()

            b.created_date = timezone.now()
            b.save()
            return redirect('AccionInm-detail', pk=b.pk)

        
    else:
        form = AccionInmForm(initial={'text':post.text})
    return render(request, 'moduloNC/nueva_AccInm.html', {'form': form})

def AccionInm_publicar(request, pk):
    #Solo los usuarios editores pueden publicar.
    post = get_object_or_404(AccionInm, pk=pk)
    usuario_req = request.user.username
    usuario_Ai = post.autor
    grupo = request.user.groups.filter(name='Editor_Responsable').exists()
    if not grupo:
        return HttpResponse("Tiene que tener un usuario con perfil de editor. " + str(usuario_req))
    if request.method == "POST":
        
        if grupo:
            formE = AccionInmFormEditor(request.POST,instance=post)
            if formE.is_valid():
                
                post2 = formE.save(commit=False)
                
            
                post2.save()
                #Si se cambia el estado a publicado, tiene que cambiar todos los
                #otros ingresos de AI de la misma NC a no publicado.
                if post2.publicado == True:
                    print("publicado")
                    nc = post2.nc
                    print(nc)
                    otrasAI = AccionInm.objects.filter(nc = nc).exclude(pk=post2.pk)
                    otrasAI.update(publicado=False)

                return redirect('AccionInm-detail', pk=post2.pk)
        
    else:
        form = AccionInmForm(instance=post)
        formE = AccionInmFormEditor(instance=post)
    return render(request, 'moduloNC/nueva_AccInm.html', {'form': form,'formE':formE})


class AccionInmDetailView(generic.DetailView):
    model = AccionInm


def accionInm_por_NC(request):
    #detalla las acc. inm por la NC 
    nc_requerida = request.GET['NC']
    nc_buscada = NC.objects.get(pk=nc_requerida)
    acc = AccionInm.objects.filter(nc=nc_buscada)
    return render(request, 'moduloNC/ac_inm_x_nc.html', {'ai':acc,'nc': nc_requerida})

class AnalisisCausaDetailView(generic.DetailView):
    model = AnalisisCausa


def analisiscausa_new(request,pk):
    nc = NC.objects.get(pk=pk)
    if request.method == "POST":
        form = AnalisisForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            if nc.autor != post.autor:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()
                    
            post.nc = nc
            post.save()
            return redirect('AnalisisCausa-detail', pk=post.pk)
    else:
        
        form = AnalisisForm()
    return render(request, 'moduloNC/nuevaAnalisis.html', {'form': form,'nc':nc})


    
def analisiscausa_por_NC(request):
    #detalla los analisis de causa por  NC 
    nc_requerida = request.GET['NC']
    nc_buscada = NC.objects.get(pk=nc_requerida)
    ac = AnalisisCausa.objects.filter(nc=nc_buscada)
    return render(request, 'moduloNC/analisiscausa_x_nc.html', {'ac':ac,'nc': nc_requerida})


def AnalisisCausa_publicar(request, pk):
    #Solo los usuarios editores pueden publicar.
    post = get_object_or_404(AnalisisCausa, pk=pk)
    usuario_req = request.user.username
    usuario_Ai = post.autor
    grupo = request.user.groups.filter(name='Editor_Responsable').exists()
    if not grupo:
        return HttpResponse("Tiene que tener un usuario con perfil de editor. " + str(usuario_req))
    if request.method == "POST":
        
        if grupo:
            formE = AnalisisFormEditor(request.POST,instance=post)
            if formE.is_valid():
                
                post2 = formE.save(commit=False)
                
            
                post2.save()
                #Si se cambia el estado a publicado, tiene que cambiar todos los
                #otros ingresos de AI de la misma NC a no publicado.
                if post2.publicado == True:
                    print("publicado")
                    nc = post2.nc
                    print(nc)
                    otrasAC = AnalisisCausa.objects.filter(nc = nc).exclude(pk=post2.pk)
                    otrasAC.update(publicado=False)

                return redirect('AnalisisCausa-detail', pk=post2.pk)
        
    else:
        form = AnalisisForm(instance=post)
        formE = AnalisisFormEditor(instance=post)
    return render(request, 'moduloNC/nuevaAnalisis.html', {'form': form,'formE':formE})

def AnalisisCausa_edit(request, pk):
    #Editar en realidad tiene que ser crear una nueva instancia sobre otra anterior
    post = get_object_or_404(AnalisisCausa, pk=pk)
    nc = post.nc
    if request.method == "POST":
        form = AnalisisForm(request.POST)
        
        if form.is_valid():
            b= form.save(commit=False)
            b.autor = request.user
            b.nc = nc

            if nc.autor != request.user:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()

            
            b.save()
            return redirect('AnalisisCausa-detail', pk=b.pk)

        
    else:
        form = AccionInmForm(initial={'descr':post.descr})
    return render(request, 'moduloNC/nuevaAnalisis.html', {'form': form})

#Acción Correctiva

class AccionCorrectivaDetailView(generic.DetailView):
    model = AccionCorrectiva


def accioncorrectiva_new(request,pk):
    nc = NC.objects.get(pk=pk)
    if request.method == "POST":
        form = AccionCorrectivaForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            if nc.autor != post.autor:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()
                    
            post.nc = nc
            post.save()
            return redirect('AccionCorrectiva-detail', pk=post.pk)
    else:
        
        form = AccionCorrectivaForm()
    return render(request, 'moduloNC/nuevaAccionCorrectiva.html', {'form': form,'nc':nc})


    
def accioncorrectiva_por_NC(request):
    #detalla la acc corr por  NC 
    nc_requerida = request.GET['NC']
    nc_buscada = NC.objects.get(pk=nc_requerida)
    ac = AccionCorrectiva.objects.filter(nc=nc_buscada)
    return render(request, 'moduloNC/accioncorrectiva_x_nc.html', {'ac':ac,'nc': nc_requerida})


def AccionCorrectiva_publicar(request, pk):
    #Solo los usuarios editores pueden publicar.
    post = get_object_or_404(AccionCorrectiva, pk=pk)
    usuario_req = request.user.username
    usuario_Ai = post.autor
    grupo = request.user.groups.filter(name='Editor_Responsable').exists()
    if not grupo:
        return HttpResponse("Tiene que tener un usuario con perfil de editor. " + str(usuario_req))
    if request.method == "POST":
        
        if grupo:
            formE = AccionCorrectivaFormEditor(request.POST,instance=post)
            if formE.is_valid():
                
                post2 = formE.save(commit=False)
                
            
                post2.save()
                #Si se cambia el estado a publicado, tiene que cambiar todos los
                #otros ingresos de AI de la misma NC a no publicado.
                if post2.publicado == True:
                    print("publicado")
                    nc = post2.nc
                    print(nc)
                    otrasAC = AccionCorrectiva.objects.filter(nc = nc).exclude(pk=post2.pk)
                    otrasAC.update(publicado=False)

                return redirect('AccionCorrectiva-detail', pk=post2.pk)
        
    else:
        form = AccionCorrectivaForm(instance=post)
        formE = AccionCorrectivaFormEditor(instance=post)
    return render(request, 'moduloNC/nuevaAccionCorrectiva.html', {'form': form,'formE':formE})

def AccionCorrectiva_edit(request, pk):
    #Editar en realidad tiene que ser crear una nueva instancia sobre otra anterior
    post = get_object_or_404(AccionCorrectiva, pk=pk)
    nc = post.nc
    if request.method == "POST":
        form = AccionCorrectivaForm(request.POST)
        
        if form.is_valid():
            b= form.save(commit=False)
            b.autor = request.user
            b.nc = nc

            if nc.autor != request.user:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()

            
            b.save()
            return redirect('AccionCorrectiva-detail', pk=b.pk)

        
    else:
        form = AccionInmForm(initial={'text':post.text})
    return render(request, 'moduloNC/nuevaAccionCorrectiva.html', {'form': form})

#Verificación AC

class VerificaACDetailView(generic.DetailView):
    model = VerificaAC


def verificacionAC_new(request,pk):
    #Se hace solo verificacion si hay una AC publicada y se hacen verificaciones solo sobre la misma.
    ac = AccionCorrectiva.objects.get(pk=pk)
    nc = ac.nc
    print(nc.pk)
    if request.method == "POST":
        form = VerificaACForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #Buscar como filtrar la AC que está publicada para la NC correspondiente.
            post.nc = nc
            post.ac = ac
        
            post.save()
            return redirect('VerificaAC-detail', pk=post.pk)
        else:
            print("no es valido")
    else:
        
        form = VerificaACForm()
        
    return render(request, 'moduloNC/nuevaVerificacionAC.html', {'form': form,'ac':ac})


    
def verificacionAC_por_AC(request):
    #detalla la verificación de AC por  NC 
    pk_ac = request.GET['AC']
    ac = AccionCorrectiva.objects.get(pk=pk_ac)
    vac = VerificaAC.objects.filter(ac=ac) 
    
    return render(request, 'moduloNC/verificacionAC_x_ac.html', {'vac':vac,'ac': ac})


def verificacion_publicar(request, pk):
    #Solo los usuarios editores pueden publicar.
    post = get_object_or_404(VerificaAC, pk=pk)
    usuario_req = request.user.username
    
    grupo = request.user.groups.filter(name='Editor_Responsable').exists()
    if not grupo:
        return HttpResponse("Tiene que tener un usuario con perfil de editor. " + str(usuario_req))
    if request.method == "POST":
        
        if grupo:
            formE = VerificaACFormEditor(request.POST,instance=post)
            if formE.is_valid():
                
                post2 = formE.save(commit=False)
                
            
                post2.save()
                #Si se cambia el estado a publicado, tiene que cambiar todos los
                #otros ingresos de AI de la misma NC a no publicado.
                if post2.publicado == True:
                    print("publicado")
                    ac = post2.ac
                    print(ac)
                    otrasVAC = VerificaAC.objects.filter(ac = ac).exclude(pk=post2.pk)
                    otrasVAC.update(publicado=False)

                return redirect('VerificaAC-detail', pk=post2.pk)
        
    else:
        form = VerificaACForm(instance=post)
        formE = VerificaACFormEditor(instance=post)
    return render(request, 'moduloNC/nuevaVerificacionAC.html', {'form': form,'formE':formE})

def verificacion_edit(request, pk):
    #Editar en realidad tiene que ser crear una nueva instancia sobre otra anterior
    post = get_object_or_404(VerificaAC, pk=pk)
    nc = post.nc
    if request.method == "POST":
        form = VerificaACForm(request.POST)
        
        if form.is_valid():
            b= form.save(commit=False)
            b.autor = request.user
            b.nc = nc

            if nc.autor != request.user:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()

            
            b.save()
            return redirect('VerificaAC-detail', pk=b.pk)

        
    else:
        form = AccionInmForm()
    return render(request, 'moduloNC/nuevaVerificacionAC.html', {'form': form})


#Archivo

class ArchivoDetailView(generic.DetailView):
    model = Archivo


def archivo_new(request,pk):
    nc = NC.objects.get(pk=pk)
    if request.method == "POST":
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            if nc.autor != post.autor:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()
                    
            post.nc = nc
            post.save()
            return redirect('Archivo-detail', pk=post.pk)
    else:
        
        form = ArchivoForm()
    return render(request, 'moduloNC/nuevaArchivo.html', {'form': form,'nc':nc})


    
def archivo_por_NC(request):
    #detalla la archivos por  NC 
    nc_requerida = request.GET['NC']
    nc_buscada = NC.objects.get(pk=nc_requerida)
    ar = Archivo.objects.filter(nc=nc_buscada)
    return render(request, 'moduloNC/archivo_x_nc.html', {'ar':ar,'nc': nc_requerida})


def Archivo_publicar(request, pk):
    #Solo los usuarios editores pueden publicar.
    post = get_object_or_404(Archivo, pk=pk)
    usuario_req = request.user.username
    grupo = request.user.groups.filter(name='Editor_Responsable').exists()
    if not grupo:
        return HttpResponse("Tiene que tener un usuario con perfil de editor. " + str(usuario_req))
    if request.method == "POST":
        
        if grupo:
            formE = ArchivoFormEditor(request.POST,instance=post)
            if formE.is_valid():
                
                post2 = formE.save(commit=False)
                
            
                post2.save()
                #Si se cambia el estado a publicado, tiene que cambiar todos los
                #otros ingresos de AI de la misma NC a no publicado.
                if post2.publicado == True:
                    print("publicado")
                    nc = post2.nc
                    print(nc)
                    otrasAC = Archivo.objects.filter(nc = nc).exclude(pk=post2.pk)
                    otrasAC.update(publicado=False)

                return redirect('Archivo-detail', pk=post2.pk)
        
    else:
        form = ArchivoForm(instance=post)
        formE = ArchivoFormEditor(instance=post)
    return render(request, 'moduloNC/nuevaArchivo.html', {'form': form,'formE':formE})


