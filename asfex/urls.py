from django.shortcuts import redirect
from django.urls import include, path
from . import settings
from django.conf.urls.static import static


def admin_redirect(request):
    return redirect('/gestion/')


urlpatterns = [
    path('admin/', admin_redirect, name='admin_redirect'),
    path('', include('siteapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

