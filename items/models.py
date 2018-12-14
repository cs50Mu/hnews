# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urlparse import urlparse

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from datetime import timedelta
from django.utils import timezone

# Create your models here.

class HowLongAgoMixin:
    def how_long_ago(self):
        now = timezone.now()
        delta = now - self.created_at
        total_seconds = int(delta.total_seconds())
        if delta < timedelta(minutes=1):
            return '{} seconds ago'.format(total_seconds)
        elif delta < timedelta(hours=1):
            return '{} minutes ago'.format(total_seconds / 60)
        elif delta < timedelta(days=1):
            return '{} hours ago'.format(total_seconds / 3600)
        else:
            return '{} days ago'.format(total_seconds / 86400)

class Item(models.Model, HowLongAgoMixin):

    title = models.CharField(max_length=255, verbose_name='标题')
    url = models.URLField(verbose_name='链接')
#    source = models.CharField(max_length=255, verbose_name='来源')
    creator = models.ForeignKey(User, related_name='items', verbose_name='创建者')
#    points = models.IntegerField(verbose_name='评分')
    voters = models.ManyToManyField(User, through='ItemUpVote', verbose_name='投票者')
#    hidden = models.BooleanField(verbose_name='是否隐藏')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def set_upvote_flag(self, user, upvote):
        q = ItemUpVote.objects.filter(voter=user, item=self)
        is_exist = q.exists()
        if upvote:
            if not is_exist:
                ItemUpVote.objects.create(voter=user, item=self)
        else:
            if is_exist:
                q.delete()

    def get_domain_name(self):
        hostname = urlparse(self.url).hostname
        if hostname.startswith('www.'):
            return hostname[len('www.'):]
        return hostname

    def to_dict(self, user):
        return {
                'title': self.title,
                'how_long_ago': self.how_long_ago(),
                'domain_name': self.get_domain_name(),
                'upvoted':
                self.voters.filter(id=user.id).count() > 0,
                'upvote_url': reverse('items:item-set-upvote', kwargs={'item_id': self.id}),
                'comments': [comment.to_dict(user) for comment in self.comments.all()],
                }

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

class ItemUpVote(models.Model):
    voter = models.ForeignKey(User, verbose_name='投票人')
    item = models.ForeignKey(Item, verbose_name='被投票的物件')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投票日期')

class Comment(models.Model, HowLongAgoMixin):
    item = models.ForeignKey(Item, related_name='comments', verbose_name='item')
    parent = models.ForeignKey('self', related_name='replies', null=True, verbose_name='针对哪个comment的comment')
    creator = models.ForeignKey(User, related_name='comments', verbose_name='创建者')
    content = models.TextField(verbose_name='评论内容')
    voters = models.ManyToManyField(User, through='CommentUpVote', verbose_name='投票者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def set_upvote_flag(self, user, upvote):
        q = CommentUpVote.objects.filter(voter=user, comment=self)
        is_exist = q.exists()
        if upvote:
            if not is_exist:
                CommentUpVote.objects.create(voter=user, comment=self)
        else:
            if is_exist:
                q.delete()

    def to_dict(self, user):
        return {
                'content': self.content,
                'how_long_ago': self.how_long_ago(),
                'creator': self.creator.username,
                'upvoted':
                self.voters.filter(id=user.id).count() > 0,
                'upvote_url': reverse('comment-set-upvote', kwargs={'comment_id': self.id}),
                }


class CommentUpVote(models.Model):
    voter = models.ForeignKey(User, verbose_name='投票人')
    comment = models.ForeignKey(Comment, verbose_name='被投票的comment')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投票日期')
