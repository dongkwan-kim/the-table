"""xtake URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from grapp import views as gr_view
from session import views as ss_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^base/', gr_view.base),
    url(r'^$', gr_view.home),
    url(r'^table/([^/]+)/([^/]+)', gr_view.table),

    url(r'^account/', ss_view.create_account),
]
