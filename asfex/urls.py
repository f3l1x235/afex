from django.shortcuts import redirect
from django.urls import include, path


def admin_redirect(request):
    return redirect('/gestion/')


urlpatterns = [
    path('admin/', admin_redirect, name='admin_redirect'),
    path('', include('siteapp.urls')),
]
