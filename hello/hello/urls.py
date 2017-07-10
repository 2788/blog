"""hello URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from blog.views import blog_index,signup,signin,logout_view,edit, edit_num, page_view , blog_view,delete

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',blog_view,name='home'),
    url(r'^signin/$', signin, name='signin'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^logout/$', logout_view, name='logout_view'),
    url(r'^edit/$', edit, name='edit'),
    url(r'^(?P<blog_number>\d+)$', blog_view,name = "blog"),
    url(r'^page/(?P<page_number>\d+)$', page_view,name = "page"),
    url(r'^edit/(?P<page_id>\d+)$', edit_num,name = "edit_num"),
    url(r'^delete/(?P<page_id>\d+)$', delete,name = "delete"),


]
