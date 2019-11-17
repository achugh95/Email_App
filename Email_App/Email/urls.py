from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^email$', views.send_email, name='Send Email'),
]
