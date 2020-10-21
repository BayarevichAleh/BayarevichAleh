from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('category/<int:category_id>', CategoryView.as_view(), name='category'),
    path('users/', UsersView.as_view(), name='users'),
    path('forum/<int:forum_id>', ForumView.as_view(), name='forum'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('forum/<int:forum_id>/add_message', AddMessageView.as_view(), name='add_message'),
    path('create_forum/', CreateForumView.as_view(), name='add_forum'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('user/<str:username>', UserView.as_view(), name='user'),
    path('forum/<int:forum_id>/edit_message/<int:pk>', EditMessageView.as_view(), name='edit_message'),
    path('myforums/', MyForumsView.as_view(), name='myforums'),
    path('forum/<int:pk>/edit_forum/', EditForumView.as_view(), name='edit_forum'),
    path('editmyprofil/', EditMyProfilView.as_view(), name='edit_my_profil'),
    path('changepassword/',UserPasswordChangeView.as_view(),name='change_password')
]
