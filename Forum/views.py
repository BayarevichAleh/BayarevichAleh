from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.views.generic.edit import BaseCreateView

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
        if context['forum'].is_pablished == False and self.request.user != context['forum'].creator:
            raise Http404('Форум не найден')
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
        form = RegForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=True)
            note.groups.set([3])
            note.save()
        else:
            return super(RegPage, self).post(request, args, kwargs)
        return redirect('index')


class AddMessage(MyAuthorization, TemplateView):
    """
    show page with form of add message
    """
    template_name = 'Forum/add_message.html'
    title = ''
    userform = UserLoginForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(AddMessage, self).get_context_data(**kwargs)
        context['userform'] = self.userform
        context['form'] = AddMessageForm
        try:
            context['forum'] = Forum.objects.get(pk=self.kwargs['forum_id'])
        except:
            return get_object_or_404(Forum, pk=self.kwargs['forum_id'])
        context['title'] = context['forum'].name
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


class EditMessage(UpdateView):
    """
    show page with form to edit forum
    """
    template_name = 'Forum/add_message.html'
    form_class = AddMessageForm
    queryset = Message.objects

    def get_success_url(self, **kwargs):
        return reverse_lazy('forum', kwargs={'forum_id': self.kwargs['forum_id']})

    def get_context_data(self, **kwargs):
        context = super(EditMessage, self).get_context_data(**kwargs)
        context['forum'] = Forum.objects.get(pk=self.kwargs['forum_id'])
        context['title'] = "Редактирование сообщения"
        return context

    def get(self, request, *args, **kwargs):
        if request.user.pk == None:
            return redirect('index')
        message = Message.objects.get(pk=self.kwargs['pk'])
        user = request.user
        if message.id_user == user:
            return super(EditMessage, self).get(request, *args, **kwargs)
        raise Http404('Ошибка атентификации')

    # def post(self, request, *args, **kwargs):
    #     message = Message.objects.get(pk=self.kwargs['pk'])
    #     user = request.user
    #     if message.id_user == user:
    #         return super(EditMessage, self).post(request, *args, **kwargs)
    #     raise Http404('Ошибка атентификации')


# class EditMessage(MyAuthorization, TemplateView):
#     template_name = 'Forum/add_message.html'
#     title = ''
#     userform = UserLoginForm
#     success_url = reverse_lazy('index')
#
#     def get_context_data(self, **kwargs):
#         context = super(EditMessage, self).get_context_data(**kwargs)
#         context['userform'] = self.userform
#         try:
#             context['forum'] = Forum.objects.get(pk=self.kwargs['forum_id'])
#         except:
#             return get_object_or_404(Forum, pk=self.kwargs['forum_id'])
#         context['title'] = context['forum'].name
#         return context
#
#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data()
#         try:
#             edit = request.GET['edit']
#         except:
#             return redirect('index')
#         if edit != None:
#             user = request.user
#             message = Message.objects.get(pk=edit)
#             if message.id_user == user:
#                 context['form'] = AddMessageForm(instance=message)
#                 return self.render_to_response(context)
#             else:
#                 raise Http404('Ошибка атентификации')
#
#     def post(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         forum = Forum.objects.get(pk=self.kwargs['forum_id'])
#         user = request.user
#         try:
#             edit = request.GET['edit']
#         except:
#             return redirect('index')
#         message = Message.objects.get(pk=edit)
#         user = request.user
#         if message.id_user == user:
#             form = AddMessageForm(request.POST, instance=message)
#             if form.is_valid():
#                 message = form.save()
#                 return HttpResponseRedirect(f"/forum/{self.kwargs['forum_id']}")
#             else:
#                 form = AddMessageForm(instance=message)
#                 return HttpResponseRedirect(f"/forum/{self.kwargs['forum_id']}")
#         raise Http404('Ошибка атентификации')


class CreateForum(CreateView):
    """
    show page with form to create forum
    """
    template_name = 'Forum/create_forum.html'
    title = 'Создать форум'
    form_class = CreateForumForm
    userform = UserLoginForm
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if request.user.pk == None:
            return redirect('index')
        else:
            return super(CreateForum, self).get(request, *args, **kwargs)


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
        raise Http404('Ошибка атентификации')


class UserPage(MyAuthorization, TemplateView):
    template_name = 'Forum/user.html'
    title = 'Пользователь'
    userform = UserLoginForm
    success_url = reverse_lazy('users')

    def get_context_data(self, *args, **kwargs):
        context = super(UserPage, self).get_context_data(**kwargs)
        context['userform'] = self.userform
        try:
            context['user'] = Users.objects.get(username=self.kwargs['username'])
        except:
            return get_object_or_404(Users, username=self.kwargs['username'])
        context['user_forums'] = Forum.objects.filter(creator=context['user'])

        context['title'] = f"Пользователь :: {context['user']}"
        return context


class MyForums(MyListView):
    model = Forum
    template_name = 'Forum/myforums.html'
    context_object_name = 'forums'
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(__class__, self).get_context_data()
        context['category'] = 'Мои форумы'
        context['title'] = "Мои форумы"
        self.pages = context['page_obj']
        context['pages'] = self.get_pages()
        return context

    def get(self, request, *args, **kwargs):
        if request.user.pk == None:
            return redirect('index')
        return super(MyForums, self).get(request, *args, **kwargs)

    def get_queryset(self):
        try:
            return Forum.objects.filter(creator=self.request.user)
        except:
            raise Http404("Ошибка авторизации")


class EditForum(UpdateView):
    """
    show page with form to edit forum
    """
    template_name = 'Forum/create_forum.html'
    form_class = CreateForumForm
    queryset = Forum.objects
    success_url = reverse_lazy('myforums')

    def get_context_data(self, **kwargs):
        context = super(EditForum, self).get_context_data(**kwargs)
        context['title'] = "Редактирование форума"
        return context

    def get(self, request, *args, **kwargs):
        if request.user.pk == None:
            return redirect('index')
        if request.user.pk == None:
            return redirect('index')
        forum = Forum.objects.get(pk=self.kwargs['pk'])
        user = request.user
        if forum.creator == user:
            return super(EditForum, self).get(request, *args, **kwargs)
        raise Http404('Ошибка атентификации')
