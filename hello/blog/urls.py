from django.conf.urls import url

urlpatterns = [
    url(r'^blog/$',blog.views.blog_index,'blog_index')
]
