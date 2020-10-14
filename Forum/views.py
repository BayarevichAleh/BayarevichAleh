from django.http import HttpResponse, Http404
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
    show HomePage
    """
    template_name = 'Forum/index.html'
    title = 'Главная страница'


class CategoriesPage(MyListView):
    """
    show page with categories
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
    """
    show page with forums of selected category or all forums if category_id = 0
    """
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
            return Forum.objects.filter(category_id=self.kwargs['category_id'], is_pablished=True)
        else:
            return Forum.objects.all()


class UsersPage(MyListView):
    """
    show page with all users
    """
    model = Users
    title = 'Пользователи'
    context_object_name = 'users'
    template_name = 'Forum/users.html'
    allow_empty = False
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersPage, self).get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        self.pages = context['page_obj']
        context['pages'] = self.get_pages()
        return context


class ForumPage(MyListView):
    """
    show page with selected forum
    """
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
        return (Message.objects.filter(id_forum=self.kwargs['forum_id']))

    def get(self, request, *args, **kwargs):
        context = super(MyListView, self).get(request, *args, **kwargs)
        try:
            delete = request.GET['delete']
        except:
            return context
        if delete != None:
            user = request.user
            message = Message.objects.get(pk=delete)
            if message.id_user == user:
                message.delete()
                return HttpResponseRedirect(f"{self.kwargs['forum_id']}")
            else:
                raise Http404('Ошибка атентификации')


class RegPage(CreateView):
    """
    show page with form of registration user
    """
    template_name = 'Forum/registration.html'
    form_class = RegForm
    title = 'Регистрация пользователя'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        """
        add default group = 3 (user)
        """
        form = RegForm(request.POST,request.FILES)
        if form.is_valid():
            note = form.save(commit=True)
            note.groups.set([3])
            note.save()
        else:
            return super(RegPage, self).post(request,args,kwargs)
        return redirect('index')



class AddMessage(MyAuthorization, TemplateView):
    """
    show page with form of add message
    """
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
        return Http404


class CreateForum(MyAuthorization, TemplateView):
    """
    show page with form to create forum
    """
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
        return Http404


class AddCategory(MyAuthorization, TemplateView):
    """
    show page with form to add category
    """
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
        return Http404


class UserPage(MyAuthorization, TemplateView):
    template_name = 'Forum/user.html'
    title = 'Пользователь'
    userform = UserLoginForm
    success_url = reverse_lazy('users')

    def get_context_data(self, *args, **kwargs):
        context = super(UserPage, self).get_context_data(**kwargs)
        context['userform'] = self.userform
        try:
            context['user'] = Users.objects.get(pk=self.kwargs['user_id'])
        except:
            return get_object_or_404(Users, pk=self.kwargs['user_id'])
        context['user_forums'] = Forum.objects.filter(creator=self.kwargs['user_id'])

        context['title'] = f"Пользователь :: {context['user']}"
        return context
