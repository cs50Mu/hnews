# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse

from items.models import Item

# Create your views here.

class ItemListView(ListView):

    template_name = 'items/list.html'
    model = Item
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['items'] = json.dumps([
            {
                'title': item.title,
                'how_long_ago': item.how_long_ago(),
                'domain_name': item.get_domain_name(),
                'upvoted':
                item.voters.filter(id=self.request.user.id).count() > 0,
                'upvote_url': reverse('items:item-set-upvote', kwargs={'item_id': item.id}),
                }
            for item in context['items']
            ])
        return context

@require_POST
@login_required
def item_set_upvote(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, KeyError):
        return HttpResponseBadRequest()
    upvote = data['upvote']
    item.set_upvote_flag(request.user, upvote)
    return HttpResponse(status=204)
