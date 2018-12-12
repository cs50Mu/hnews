# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mock import patch, MagicMock
import pytest
from datetime import datetime, timedelta
import pytz
import json

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

from . models import Item, Comment

# Create your tests here.

class TestHowLongAgo:

    def setup(self):
        self.create_time = datetime(2018, 10, 12, tzinfo=pytz.utc)

    def test_0_seconds_ago(self):
        item = Item(created_at=self.create_time)
        with patch('items.models.timezone') as dt:
            dt.now = MagicMock()
            dt.now.return_value = self.create_time
            assert item.how_long_ago() == '0 seconds ago'

    def test_x_seconds_ago(self):
        item = Item(created_at=self.create_time)
        with patch('items.models.timezone') as dt:
            dt.now = MagicMock()
            dt.now.return_value = self.create_time + timedelta(seconds=5)
            assert item.how_long_ago() == '5 seconds ago'

    def test_1_mins_ago(self):
        create_time = datetime(2018, 10, 12)
        item = Item(created_at=self.create_time)
        with patch('items.models.timezone') as dt:
            dt.now = MagicMock()
            dt.now.return_value = self.create_time + timedelta(minutes=1)
            assert item.how_long_ago() == '1 minutes ago'

    def test_x_mins_ago(self):
        create_time = datetime(2018, 10, 12)
        item = Item(created_at=self.create_time)
        with patch('items.models.timezone') as dt:
            dt.now = MagicMock()
            dt.now.return_value = self.create_time + timedelta(minutes=7)
            assert item.how_long_ago() == '7 minutes ago'

    def test_x_hours_ago(self):
        create_time = datetime(2018, 10, 12)
        item = Item(created_at=self.create_time)
        with patch('items.models.timezone') as dt:
            dt.now = MagicMock()
            dt.now.return_value = self.create_time + timedelta(hours=7)
            assert item.how_long_ago() == '7 hours ago'

    def test_x_days_ago(self):
        create_time = datetime(2018, 10, 12)
        item = Item(created_at=self.create_time)
        with patch('items.models.timezone') as dt:
            dt.now = MagicMock()
            dt.now.return_value = self.create_time + timedelta(days=17)
            assert item.how_long_ago() == '17 days ago'

def test_domain_name():
    item = Item(url='https://techcrunch.com/2018/06/05/washington-sues-facebook-and-google-over-failure-to-disclose-political-ad-spending/')
    assert item.get_domain_name() == 'techcrunch.com'

def test_domain_name_with_subdomain():
    item = Item(url='https://blog.mozilla.org/nnethercote/2018/06/05/how-to-speed-up-the-rust-compiler-some-more-in-2018/')
    assert item.get_domain_name() == 'blog.mozilla.org'

def test_domain_name_with_www():
    item = Item(url='https://www.livescience.com/61627-ancient-virus-brain.html')
    assert item.get_domain_name() == 'livescience.com'

@pytest.mark.django_db
def test_set_upvote_true():
    user = User.objects.create_user(username='linuxfish', email='linux@wonderland.com', password='hard')
    item = Item.objects.create(title='google', url='http://www.google.com', creator=user)
    item.set_upvote_flag(user, True)
    # item.voters是一个models.Manager类
    # https://docs.djangoproject.com/en/2.1/topics/db/queries/#following-relationships-backward
    assert item.voters.count() == 1

@pytest.mark.django_db
def test_set_upvote_false():
    user = User.objects.create_user(username='linuxfish', email='linux@wonderland.com', password='hard')
    item = Item.objects.create(title='google', url='http://www.google.com', creator=user)
    item.set_upvote_flag(user, True)
    item.set_upvote_flag(user, False)
    assert item.voters.count() == 0

class TestComment:

    @pytest.mark.django_db
    def test_set_upvote_true(self):
        user = User.objects.create_user(username='linuxfish', email='linux@wonderland.com', password='hard')
        tom = User.objects.create_user(username='tom', email='tome@wonderland.com', password='hard')
        item = Item.objects.create(title='google', url='http://www.google.com', creator=user)
        comment = Comment.objects.create(item=item, creator=user, content='good article')
        comment.set_upvote_flag(tom, True)
        assert comment.voters.count() == 1

    @pytest.mark.django_db
    def test_set_upvote_false(self):
        user = User.objects.create_user(username='linuxfish', email='linux@wonderland.com', password='hard')
        tom = User.objects.create_user(username='tom', email='tome@wonderland.com', password='hard')
        item = Item.objects.create(title='google', url='http://www.google.com', creator=user)
        comment = Comment.objects.create(item=item, creator=user, content='good article')
        comment.set_upvote_flag(tom, True)
        assert comment.voters.count() == 1
        comment.set_upvote_flag(tom, False)
        assert comment.voters.count() == 0

@pytest.mark.django_db
def test_view_set_upvote_true():
    user = User.objects.create_user(username='linuxfish', email='linux@wonderland.com', password='hard')
    item = Item.objects.create(title='google', url='http://www.google.com', creator=user)
    client = Client()
    client.login(username='linuxfish', password='hard')
    # reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None)
    # viewname can be a URL pattern name or the callable view object
    # ref: https://docs.djangoproject.com/en/1.11/ref/urlresolvers/#django.urls.reverse
    uri = reverse('items:item-set-upvote', kwargs={'item_id': item.id})
    client.post(uri, json.dumps({'upvote': True}), content_type='application/json')
    assert item.voters.count() == 1

@pytest.mark.django_db
def test_view_set_upvote_false():
    user = User.objects.create_user(username='linuxfish', email='linux@wonderland.com', password='hard')
    item = Item.objects.create(title='google', url='http://www.google.com', creator=user)
    client = Client()
    client.login(username='linuxfish', password='hard')
    # reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None)
    # viewname can be a URL pattern name or the callable view object
    # ref: https://docs.djangoproject.com/en/1.11/ref/urlresolvers/#django.urls.reverse
    uri = reverse('items:item-set-upvote', kwargs={'item_id': item.id})
    assert item.voters.count() == 0
    client.post(uri, json.dumps({'upvote': True}), content_type='application/json')
    assert item.voters.count() == 1
    client.post(uri, json.dumps({'upvote': False}), content_type='application/json')
    assert item.voters.count() == 0
