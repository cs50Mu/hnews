# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseBadRequest

from items.models import Item, Comment
from items.forms import CommentForm

# Create your views here.

class ItemListView(ListView):

    template_name = 'items/list.html'
    model = Item
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['items'] = json.dumps([
            item.to_dict(self.request.user)
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

@require_POST
@login_required
def comment_add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, KeyError):
        return HttpResponseBadRequest()
    comment = Comment(parent=comment,
            item=comment.item,
            content=data['content'],
            creator=request.user)
    comment.save()
    return HttpResponse(status=204)

@require_POST
@login_required
def comment_set_upvote(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, KeyError):
        return HttpResponseBadRequest()
    upvote = data['upvote']
    comment.set_upvote_flag(request.user, upvote)
    return HttpResponse(status=204)

class CommentCreateView(CreateView):
    template_name = 'items/create.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        return login_required(super(CreateView, self).post)(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        context['item_json'] = json.dumps(
                self.item.to_dict(self.request.user))
        context['item'] = self.item
        return context

    def dispatch(self, request, *args, **kwargs):
        self.item = get_object_or_404(Item, id=kwargs['item_id'])
        return super(CommentCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.item = self.item
        obj.save()
        return self.render_to_response(self.get_context_data())
