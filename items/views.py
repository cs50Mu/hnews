# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.list import ListView

from items.models import Item

# Create your views here.

class ItemListView(ListView):

    template_name = 'items/list.html'
    model = Item
    context_object_name = 'items'
