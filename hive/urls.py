from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'hive'
urlpatterns = [
    path('', views.index, name='index'),
    path('save/<str:name>/<str:value>/', views.save, name='save'),
    path('send/<str:name>/', views.send, name='send'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
