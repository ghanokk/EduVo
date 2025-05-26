from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.homePage, name='homePage'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)