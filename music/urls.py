from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns=[path('',views.IndexView.as_view(),name='index'),
             path('register',views.UserFormView.as_view(),name='register'),
             path('<pk>',views.DetailView.as_view(),name='details'),
             path('<pk>/favourite', views.favourite, name='favourite'),
             path('album/add/',views.Albumcreate.as_view(),name='album-add'),
             path('album/<int:pk>/', views.AlbumUpdate.as_view(), name='album-update'),
             path('album/<int:pk>/delete', views.Albumdelete.as_view(), name='album-delete'),]

