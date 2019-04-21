# Create your views here.

from django.shortcuts import render
from .models import NC
from django.views import generic

# Create your views here.

def index(request):
    nc = NC.objects.all().count()
    nc_fin = NC.objects.filter(cerrada = True).count()
    return render(request, 'moduloNC/index.html', {'nc':nc,'nc_fin': nc_fin})

class NCListView(generic.ListView):
    model = NC

class NCDetailView(generic.DetailView):
    model = NC