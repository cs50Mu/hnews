# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Item(models.Model):

    title = models.CharField(max_length=255, verbose_name='标题')
    url = models.URLField(verbose_name='链接')
    source = models.CharField(max_length=255, verbose_name='来源')
    creator = models.CharField(max_length=255, verbose_name='创建者')
    points = models.IntegerField(verbose_name='评分')
    hidden = models.BooleanField(verbose_name='是否隐藏')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
