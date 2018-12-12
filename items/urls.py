from django.conf.urls import url, include

from . import views

app_name = 'items'
urlpatterns = [
        url(r'^$', views.ItemListView.as_view(), name='list'),
        url(r'^(?P<item_id>\d+)/set_upvote/?$', views.item_set_upvote, name='item-set-upvote'),
        ]
