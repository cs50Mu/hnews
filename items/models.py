# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):

    title = models.CharField(max_length=255, verbose_name='标题')
    url = models.URLField(verbose_name='链接')
    source = models.CharField(max_length=255, verbose_name='来源')
    creator = models.ForeignKey(User, related_name='items', verbose_name='创建者')
    points = models.IntegerField(verbose_name='评分')
    voters = models.ManyToManyField(User, through='ItemUpVote', verbose_name='投票者')
    hidden = models.BooleanField(verbose_name='是否隐藏')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

class ItemUpVote(models.Model):
    voter = models.ForeignKey(User, verbose_name='投票人')
    item = models.ForeignKey(Item, verbose_name='被投票的物件')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投票日期')

class Comment(models.Model):
    item = models.ForeignKey(Item, related_name='comments', verbose_name='item')
    parent = models.ForeignKey('self', related_name='replies', verbose_name='针对哪个comment的comment')
    creator = models.ForeignKey(User, related_name='comments', verbose_name='创建者')
    content = models.TextField(verbose_name='评论内容')
    voters = models.ManyToManyField(User, through='CommentUpVote', verbose_name='投票者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

class CommentUpVote(models.Model):
    voter = models.ForeignKey(User, verbose_name='投票人')
    comment = models.ForeignKey(Comment, verbose_name='被投票的comment')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投票日期')
