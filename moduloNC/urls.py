from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('nc/', views.NCListView.as_view(), name='nc'),
    path('nc/<int:pk>/',views.NCDetailView.as_view(),name='nc-detail'),
    path('nuevanc', views.nc_new, name='nuevanc'),

]
