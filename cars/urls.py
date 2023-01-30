from django.urls import path

from . import views

urlpatterns = [
    path('', views.newindex, name='index'),
    path('create/', views.createCar, name='create'),
    path('delete/<int:pk>/', views.deleteCar, name='delete'),
    path('update/<int:pk>/', views.updateCar, name='update'),
    path('up/<int:pk>/', views.up, name='up'),
    path('down/<int:pk>/', views.down, name='down'),
]
