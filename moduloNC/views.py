# Create your views here.

from django.shortcuts import render
from .models import NC, AccionInm
from django.views import generic
from .forms import NCForm,AccionInmForm
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
            post.nc = nc
            post.save()
            return redirect('AccionInm-detail', pk=post.pk)
    else:
        
        form = AccionInmForm()
    return render(request, 'moduloNC/nueva_AccInm.html', {'form': form,'nc':nc})

def AccionInm_edit(request, pk):
    post = get_object_or_404(AccionInm, pk=pk)
    usuario_req = request.user.username
    usuario_Ai = post.autor
    if str(usuario_Ai) != str(usuario_req):
        return HttpResponse("Tiene que ser el creador de la AI ("+str(usuario_Ai) +") para poder editarla.")
    if request.method == "POST":
        form = AccionInmForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()
            return redirect('AccionInm-detail', pk=post.pk)
    else:
        form = AccionInmForm(instance=post)
    return render(request, 'moduloNC/nueva_AccInm.html', {'form': form})


class AccionInmDetailView(generic.DetailView):
    model = AccionInm


def accionInm_por_NC(request):
    #detalla las acc. inm por la NC 
    nc_requerida = request.GET['NC']
    nc_buscada = NC.objects.get(pk=nc_requerida)
    acc = AccionInm.objects.filter(nc=nc_buscada)
    return render(request, 'moduloNC/ac_inm_x_nc.html', {'ai':acc,'nc': nc_requerida})