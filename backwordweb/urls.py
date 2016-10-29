from django.conf.urls import url
from django.conf import settings
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register_view, name='register_view'),
    url(r'^login$', views.login_view, name='login_view'),
    url(r'^logout$', views.logout_view, name='logout_view'),
    url(r'^info$', views.info_view, name='info_view'),
    url(r'^backword$', views.backword_view, name='backword_view'),
    url(r'^addnote$', views.addnote, name='addnote'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_URL}),
]
