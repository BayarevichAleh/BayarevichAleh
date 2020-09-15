from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from .models import *
from .forms import *


# class index(TemplateView):
#     template_name = "index.html"

class HomePage(TemplateView):
    template_name = 'Forum/index.html'
    context = {'title':'Мой первый сайт'}



class CategoriesPage(ListView):
    model = Category
    template_name = 'Forum/categories.html'
    context_object_name = 'categories'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoriesPage, self).get_context_data(**kwargs)
        context['title'] = 'Категории'
        return context


class CategoryPage(ListView):
    model = Forum
    template_name = 'Forum/category.html'
    context_object_name = 'forums'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryPage, self).get_context_data(**kwargs)
        context['title'] = 'Категории'
        if self.kwargs['category_id'] != 0:
            context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
        else:
            context['category'] = 0
        return context

    def get_queryset(self):
        if self.kwargs['category_id'] != 0:
            return Forum.objects.filter(category_id=self.kwargs['category_id'])
        else:
            return Forum.objects.all()


class UserPage(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'Forum/users.html'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserPage, self).get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        return context


# Create your views here.
class ForumPage(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'Forum/forum.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ForumPage, self).get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        try:
            context['forum'] = Forum.objects.get(pk=self.kwargs['forum_id'])
        except:
            return get_object_or_404(Forum, pk=self.kwargs['forum_id'])

        return context

    def get_queryset(self):
        return Message.objects.filter(id_forum=self.kwargs['forum_id'])



class RegPage(CreateView):
    form_class = RegForm
    template_name = 'Forum/registration.html'
    success_url = reverse_lazy('index')
