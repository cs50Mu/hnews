"""hnews URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from items.views import comment_set_upvote, comment_add_reply

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # namespaced URLs
    # ref: https://docs.djangoproject.com/en/1.11/topics/http/urls/#id4
    url(r'^items/', include('items.urls', namespace='items')),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^comments/(?P<comment_id>\d+)/set_upvote', comment_set_upvote, name='comment-set-upvote'),
    url(r'^comments/(?P<comment_id>\d+)/add_reply', comment_add_reply, name='comment-add_reply'),
]
