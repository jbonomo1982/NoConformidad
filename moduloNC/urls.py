from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('nc/', views.NCListView.as_view(), name='nc'),
    path('nc/<int:pk>/',views.NCDetailView.as_view(),name='nc-detail'),
    path('nuevanc', views.nc_new, name='nuevanc'),
    path('nuevaAccionInm/<int:pk>/', views.AccionInm_new, name='nuevaAccionInm'),
    path('AccionInm/<int:pk>/',views.AccionInmDetailView.as_view(),name='AccionInm-detail'),
    path('accionInm_por_NC', views.accionInm_por_NC, name='accionInm_por_NC'),
    path('AccionInm_edit/<int:pk>/',views.AccionInm_edit,name='AccionInm-edit'),
    path('AccionInm_publicar/<int:pk>/',views.AccionInm_publicar,name='AccionInm-publicar'),
    path('nuevaAnalisiscausa/<int:pk>/', views.analisiscausa_new, name='nuevaAnalisis'),
    path('AnalisisCausa/<int:pk>/',views.AnalisisCausaDetailView.as_view(),name='AnalisisCausa-detail'),
    path('AnalisisCausa_por_NC', views.analisiscausa_por_NC, name='analisiscausa_por_NC'),
    path('Analisis_publicar/<int:pk>/',views.AnalisisCausa_publicar,name='Analisis-publicar'),
    path('Analisis_edit/<int:pk>/',views.AnalisisCausa_edit,name='Analisis-edit'),


]
