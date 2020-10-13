from .forms import *
from django.contrib.auth import login, logout
from django.views.generic import ListView
from django.http import Http404
from django.utils.translation import gettext as _


class Mypaginator(object):
    """
    Mixin of change pagination
    """
    pages = object

    def get_pages(self):
        if self.pages.paginator.num_pages < 10:
            return (range(1, self.pages.paginator.num_pages + 1))
        elif self.pages.number > self.pages.paginator.num_pages - 5:
            return (range(self.pages.paginator.num_pages - 8, self.pages.paginator.num_pages + 1))
        else:
            return (range(self.pages.number - 4, self.pages.number + 4))


class MyListView(ListView, Mypaginator):
    """
    chenged class ListView
    - add POST method
    """
    title = ''
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(__class__, self).get_context_data(**kwargs)
        userform = UserLoginForm
        context['userform'] = userform
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data(**kwargs)
        userform = UserLoginForm(data=request.POST)
        if userform.is_valid():
            user = userform.get_user()
            login(request, user)
        else:
            context['userform'] = userform
        return self.render_to_response(context)


class MyAuthorization(object):
    """
    Authorization class

    """
    userform = object
    title = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(__class__, self).get_context_data(**kwargs)
        userform = UserLoginForm
        context['userform'] = userform
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        userform = UserLoginForm(data=request.POST)
        if userform.is_valid():
            user = userform.get_user()
            login(request, user)
        else:
            context['userform'] = userform

        return self.render_to_response(context)
