from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Root path serves index.html
    path('api/hello/', views.hello_api, name='hello_api'),
    path('api/goodswipe/', views.goodswipe, name='goodswipe'),
    path('api/badswipe/', views.badswipe, name='badswipe'),
    path('api/getnextcandidate/', views.getnextcandidate, name='getnextcandidate'),
]
