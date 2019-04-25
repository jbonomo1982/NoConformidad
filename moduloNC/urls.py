from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('nc/', views.NCListView.as_view(), name='nc'),
    path('nc/<int:pk>/',views.NCDetailView.as_view(),name='nc-detail'),
    path('nuevanc', views.nc_new, name='nuevanc'),
    path('nuevaAccionInm', views.AccionInm_new, name='nuevaAccionInm'),
    path('AccionInm/<int:pk>/',views.AccionInmDetailView.as_view(),name='AccionInm-detail'),

]
