from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from .utils import *
from django.contrib.auth import login, logout
from django.contrib.auth.models import User


def user_logout(request):
    logout(request)
    print(request.POST.get('url'))
    return redirect(request.POST.get('url'))


class HomePage(MyAuthorization, TemplateView):
    template_name = 'Forum/index.html'
    title = 'Главная страница'


class CategoriesPage(MyListView):
    model = Category
    title = 'Категории'
    template_name = 'Forum/categories.html'
    context_object_name = 'categories'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoriesPage, self).get_context_data(**kwargs)
        self.pages = context['page_obj']
        context['pages'] = self.get_pages()
        return context


class CategoryPage(MyListView):
    model = Forum
    template_name = 'Forum/category.html'
    context_object_name = 'forums'
    allow_empty = False
    paginate_by = 5

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
            return Forum.objects.filter(category_id=self.kwargs['category_id'])
        else:
            return Forum.objects.all()


class UserPage(MyListView):
    model = Users
    title = 'Пользователи'
    context_object_name = 'users'
    template_name = 'Forum/users.html'
    allow_empty = False
    paginate_by = 5

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
    allow_empty = False
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
        return Message.objects.filter(id_forum=self.kwargs['forum_id'])


class RegPage(CreateView):
    form_class = RegForm
    template_name = 'Forum/registration.html'
    success_url = reverse_lazy('index')


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
            print(request.POST)
            return redirect('index')
        else:
            return super(AddMessage, self).get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        print(request.POST)
        forum = Forum.objects.get(pk=self.kwargs['forum_id'])
        user = request.user
        model = Message(id_forum=forum, id_user=user, text=request.POST['text'])
        model.save()
        return redirect(f"../{kwargs['forum_id']}")

# class AddMessage(TemplateView):
#     form = AddMessageForm
#     template_name = 'Forum/add_message.html'
#     success_url = reverse_lazy('index')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(AddMessage, self).get_context_data(**kwargs)
#         context['title'] = 'Пользователи'
#         try:
#             context['forum'] = Forum.objects.get(pk=self.kwargs['forum_id'])
#         except:
#             return get_object_or_404(Forum, pk=self.kwargs['forum_id'])
#
#         return context
