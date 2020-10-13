from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from .utils import *
from django.contrib.auth import login, logout
from django.contrib.auth.models import User


def user_logout(request):
    """
    logout function
    :param request:
    :return: redirect at URL last HTML page
    """
    logout(request)
    return redirect(request.POST.get('url'))


class HomePage(MyAuthorization, TemplateView):
    """
    view HomePage
    """
    template_name = 'Forum/index.html'
    title = 'Главная страница'


class CategoriesPage(MyListView):
    """
    view
    """
    model = Category
    title = 'Категории'
    template_name = 'Forum/categories.html'
    context_object_name = 'categories'
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoriesPage, self).get_context_data(**kwargs)
        self.pages = context['page_obj']
        context['pages'] = self.get_pages()
        return context


class CategoryPage(MyListView):
    model = Forum
    template_name = 'Forum/category.html'
    context_object_name = 'forums'
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(__class__, self).get_context_data(**kwargs)
        if self.kwargs['category_id'] != 0:
            context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
            context['title'] = f"Категория :: {context['category']}"
        else:
            context['category'] = 0
            context['title'] = "Категория :: Все категории"
        self.pages = context['page_obj']
        context['pages'] = self.get_pages()
        return context

    def get_queryset(self):
        if self.kwargs['category_id'] != 0:
            return Forum.objects.filter(category_id=self.kwargs['category_id'],is_pablished=True)
        else:
            return Forum.objects.all()


class UserPage(MyListView):
    model = Users
    title = 'Пользователи'
    context_object_name = 'users'
    template_name = 'Forum/users.html'
    allow_empty = False
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserPage, self).get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        self.pages = context['page_obj']
        context['pages'] = self.get_pages()
        return context


# Create your views here.
class ForumPage(MyListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'Forum/forum.html'
    allow_empty = True
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ForumPage, self).get_context_data(**kwargs)
        try:
            context['forum'] = Forum.objects.get(pk=self.kwargs['forum_id'])

        except:
            return get_object_or_404(Forum, pk=self.kwargs['forum_id'])
        context['title'] = f"Форум :: {context['forum']}"
        self.pages = context['page_obj']
        context['pages'] = self.get_pages()
        return context

    def get_queryset(self):
        return(Message.objects.filter(id_forum=self.kwargs['forum_id']))


class RegPage(TemplateView):
    template_name = 'Forum/registration.html'
    title = 'Регистрация пользователя'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(RegPage, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['form'] = RegForm
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = RegForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=True)
            note.groups.set([3,])
            note.save()
            return redirect('index')


class AddMessage(MyAuthorization, TemplateView):
    template_name = 'Forum/add_message.html'
    title = 'Главная страница'
    userform = UserLoginForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(AddMessage, self).get_context_data(**kwargs)
        context['userform'] = self.userform
        context['title'] = self.title
        context['form'] = AddMessageForm
        try:
            context['forum'] = Forum.objects.get(pk=self.kwargs['forum_id'])
        except:
            return get_object_or_404(Forum, pk=self.kwargs['forum_id'])
        return context

    def get(self, request, *args, **kwargs):
        if request.user.pk == None:
            return redirect('index')
        else:
            return super(AddMessage, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        forum = Forum.objects.get(pk=self.kwargs['forum_id'])
        user = request.user
        form = AddMessageForm(request.POST)
        if form.is_valid():
            note = form.save(commit=True)
            note.id_user = user
            note.id_forum = forum
            note.save()
            return redirect(f"../{kwargs['forum_id']}")
        return HttpResponse('De indtastede data er ikke gyldige')



class CreateForum(MyAuthorization, TemplateView):
    template_name = 'Forum/create_forum.html'
    title = 'Создать форум'
    userform = UserLoginForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(CreateForum, self).get_context_data(**kwargs)
        context['userform'] = self.userform
        context['title'] = self.title
        context['form'] = CreateForumForm
        return context

    def get(self, request, *args, **kwargs):
        if request.user.pk == None:
            return redirect('index')
        else:
            return super(CreateForum, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = CreateForumForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=True)
            note.creator = request.user
            note.save()
            # forum=Forum.objects.get(name=form['name'])
            return redirect('index')


class AddCategory(MyAuthorization, TemplateView):
    template_name = 'Forum/add_category.html'
    title = 'Добавить категорию'
    userform = UserLoginForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(AddCategory, self).get_context_data(**kwargs)
        context['userform'] = self.userform
        context['title'] = self.title
        context['form'] = AddCategoryForm
        return context

    def get(self, request, *args, **kwargs):
        if request.user.pk == None:
            return redirect('index')
        else:
            return super(AddCategory, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
