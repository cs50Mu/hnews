# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseBadRequest

from items.models import Item

# Create your views here.

class ItemListView(ListView):

    template_name = 'items/list.html'
    model = Item
    context_object_name = 'items'

@require_POST
@login_required
def item_set_upvote(request, item_id):
    import json
    item = get_object_or_404(Item, id=item_id)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, KeyError):
        return HttpResponseBadRequest()
    upvote = data['upvote']
    item.set_upvote_flag(request.user, upvote)
    return HttpResponse(status=204)
