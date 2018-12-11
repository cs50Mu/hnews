from django.conf.urls import url, include

from . import views

urlpatterns = [
        url('', views.ItemListView.as_view(), name='list'),
        ]
