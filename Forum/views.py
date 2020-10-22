from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.utils.translation import gettext as _
from django.core.mail import send_mail

from .utils import *
from .forms import *


class MyListView(ListView, MyPaginator):
    title = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(__class__, self).get_context_data(**kwargs)
        context['userform'] = UserLoginForm
        context['title'] = self.title
        self.pages = context['page_obj']
        context['pages'] = self.get_pages()
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
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


class UserLogout(TemplateView):
    template_name = 'Forum/index.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(request.GET.get('url'))


class HomePageView(TemplateView):
    template_name = 'Forum/index.html'
    title = 'Главная страница'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(__class__, self).get_context_data(**kwargs)
        context['userform'] = UserLoginForm
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


class CategoriesView(MyListView):
    model = Category
    title = 'Категории'
    template_name = 'Forum/categories.html'
    context_object_name = 'categories'
    allow_empty = True
    paginate_by = 5


class CategoryView(MyListView):
    model = Forum
    template_name = 'Forum/category.html'
    context_object_name = 'forums'
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
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
            return Forum.objects.filter(category_id=self.kwargs['category_id'], is_published=True)
        else:
            return Forum.objects.filter(is_published=True)


class UsersView(MyListView):
    model = Users
    title = 'Пользователи'
    context_object_name = 'users'
    template_name = 'Forum/users.html'
    allow_empty = False
    paginate_by = 10


class ForumView(MyListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'Forum/forum.html'
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        try:
            context['forum'] = Forum.objects.get(pk=self.kwargs['forum_id'])
        except:
            return get_object_or_404(Forum, pk=self.kwargs['forum_id'])
        if context['forum'].is_published == False and self.request.user != context['forum'].creator:
            raise Http404('Форум не найден')
        context['title'] = f"Форум :: {context['forum']}"
        self.pages = context['page_obj']
        context['pages'] = self.get_pages()
        return context

    def get_queryset(self):
        return (Message.objects.filter(id_forum=self.kwargs['forum_id']))

    def get(self, request, *args, **kwargs):
        context = super(ForumView, self).get(request, *args, **kwargs)
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


class RegistrationView(CreateView):
    template_name = 'Forum/registration.html'
    form_class = RegistrationForm
    title = 'Регистрация пользователя'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=True)
            note.groups.set([3])
            note.save()
            subject = "Регистрация на сайте - Мой первй форум"
            email_text = "Уважаемый пользователь! Вы зарегистрированы на сайте 'Мой первый форум', если вы этого не далали, просим связаться с администраторами сайта"
            try:
                send_mail(subject=subject, message=email_text, from_email='BayarevichForum@yandex.ru', recipient_list=[form.cleaned_data['email']], fail_silently=False)
            except:
                pass
        else:
            return super(RegistrationView, self).post(request, args, kwargs)
        return redirect('index')


class AddMessageView(CreateView):
    template_name = 'Forum/add_message.html'
    title = 'Добавить сообщение'
    form_class = AddMessageForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(AddMessageView, self).get_context_data(**kwargs)
        context['userform'] = UserLoginForm
        try:
            context['forum'] = Forum.objects.get(pk=self.kwargs['forum_id'])
        except:
            return get_object_or_404(Forum, pk=self.kwargs['forum_id'])
        return context

    def get(self, request, *args, **kwargs):

        if request.user.pk == None:
            return redirect('index')
        else:
            return super(AddMessageView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        forum = Forum.objects.get(pk=self.kwargs['forum_id'])
        user = request.user
        form = AddMessageForm(request.POST)
        if form.is_valid():
            note = form.save(commit=True)
            note.id_user = user
            note.id_forum = forum
            note.save()
            return redirect(f"../{kwargs['forum_id']}")
        else:
            return super(AddMessageView, self).post(request, *args, **kwargs)


class EditMessageView(UpdateView):
    template_name = 'Forum/add_message.html'
    form_class = AddMessageForm
    queryset = Message.objects

    def get_success_url(self, **kwargs):
        return reverse_lazy('forum', kwargs={'forum_id': self.kwargs['forum_id']})

    def get_context_data(self, **kwargs):
        context = super(EditMessageView, self).get_context_data(**kwargs)
        context['forum'] = get_object_or_404(Forum, pk=self.kwargs['forum_id'])
        context['title'] = "Редактирование сообщения"
        return context

    def get(self, request, *args, **kwargs):
        if request.user.pk == None:
            return redirect('index')
        message = get_object_or_404(Message, pk=self.kwargs['pk'])
        forum = get_object_or_404(Forum, pk=self.kwargs['forum_id'])
        print(forum)
        user = request.user
        if message.id_forum == forum:
            if message.id_user == user:
                return super(EditMessageView, self).get(request, *args, **kwargs)
            raise Http404('Ошибка атентификации')
        raise Http404('Страница не найдена')


class CreateForumView(CreateView):
    template_name = 'Forum/create_forum.html'
    form_class = CreateForumForm
    userform = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super(CreateForumView, self).get_context_data(**kwargs)
        context['title'] = 'Создать форум'
        return context

    def get(self, request, *args, **kwargs):
        if request.user.pk == None:
            return redirect('index')
        else:
            return super(CreateForumView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = CreateForumForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=True)
            note.creator = user
            note.save()
            return self.form_valid(form)
        else:
            return super(CreateForumView, self).post(request, *args, **kwargs)


class AddCategoryView(CreateView):
    template_name = 'Forum/add_category.html'
    form_class = AddCategoryForm
    success_url = reverse_lazy('add_forum')

    def get_context_data(self, **kwargs):
        context = super(AddCategoryView, self).get_context_data(**kwargs)
        context['userform'] = UserLoginForm
        context['title'] = 'Добавить категорию'
        return context

    def get(self, request, *args, **kwargs):
        if request.user.pk == None:
            return redirect('index')
        else:
            return super(AddCategoryView, self).get(request, *args, **kwargs)


class UserView(TemplateView):
    template_name = 'Forum/user.html'
    userform = UserLoginForm

    def get_context_data(self, *args, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['userform'] = UserLoginForm
        try:
            context['user'] = Users.objects.get(username=self.kwargs['username'])
        except:
            return get_object_or_404(Users, username=self.kwargs['username'])
        context['user_forums'] = Forum.objects.filter(creator=context['user'])

        context['title'] = f"Пользователь :: {context['user']}"
        return context


class MyForumsView(MyListView):
    model = Forum
    template_name = 'Forum/myforums.html'
    context_object_name = 'forums'
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyForumsView, self).get_context_data()
        context['category'] = 'Мои форумы'
        context['title'] = "Мои форумы"
        self.pages = context['page_obj']
        context['pages'] = self.get_pages()
        return context

    def get(self, request, *args, **kwargs):
        if request.user.pk == None:
            return redirect('index')
        return super(MyForumsView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        try:
            return Forum.objects.filter(creator=self.request.user)
        except:
            raise Http404("Ошибка авторизации")


class EditForumView(UpdateView):
    template_name = 'Forum/create_forum.html'
    form_class = CreateForumForm
    queryset = Forum.objects
    success_url = reverse_lazy('myforums')

    def get_context_data(self, **kwargs):
        context = super(EditForumView, self).get_context_data(**kwargs)
        context['title'] = "Редактирование форума"
        return context

    def get(self, request, *args, **kwargs):
        if request.user.pk == None:
            return redirect('index')
        forum = Forum.objects.get(pk=self.kwargs['pk'])
        user = request.user
        if forum.creator == user:
            return super(EditForumView, self).get(request, *args, **kwargs)
        raise Http404('Ошибка атентификации')


class EditMyProfilView(UpdateView):
    template_name = 'Forum/editmyprofil.html'
    form_class = EditUserForm

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(EditMyProfilView, self).get_context_data(**kwargs)
        context['title'] = "Редактирование профиля"
        return context

    def get(self, request, *args, **kwargs):
        if request.user.pk == None:
            return redirect('index')
        return super(EditMyProfilView, self).get(request, *args, **kwargs)


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'Forum/change_password.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('index')
