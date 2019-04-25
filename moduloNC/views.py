# Create your views here.

from django.shortcuts import render
from .models import NC, AccionInm
from django.views import generic
from .forms import NCForm,AccionInmForm
from django.shortcuts import redirect

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

def AccionInm_new(request):
    if request.method == "POST":
        form = AccionInmForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            return redirect('AccionInm-detail', pk=post.pk)
    else:
        form = AccionInmForm()
    return render(request, 'moduloNC/nueva_AccInm.html', {'form': form})

class AccionInmDetailView(generic.DetailView):
    model = AccionInm