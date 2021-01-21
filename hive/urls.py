from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'hive'
urlpatterns = [
    path('', views.index, name='index'),
    path('save/<str:name>/<str:value>/', views.save, name='save'),
    path('send/<str:name>/', views.send, name='send'),
    path('up', views.up, name='up'),
    path('down', views.down, name='down'),
    path('stop', views.stop, name='stop'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
