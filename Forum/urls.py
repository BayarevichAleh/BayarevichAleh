from django.urls import path, include
from .views import *

urlpatterns = [
    # path('', index, name='index'),
    path('', HomePage.as_view(), name='index'),
    path('categories/', CategoriesPage.as_view(), name='categories'),
    path('category/<int:category_id>', CategoryPage.as_view(), name='category'),
    path('users/', UsersPage.as_view(), name='users'),
    path('forum/<int:forum_id>', ForumPage.as_view(), name='forum'),
    path('registration/', RegPage.as_view(), name='registration'),
    path('logout/', user_logout, name='logout'),
    path('forum/<int:forum_id>/add_message', AddMessage.as_view(), name='add_message'),
    path('create_forum/', CreateForum.as_view(), name='add_forum'),
    path('add_category/', AddCategory.as_view(), name='add_category'),
    path('user/<str:username>', UserPage.as_view(), name='user'),
    path('forum/<int:forum_id>/edit_message/<int:pk>', EditMessage.as_view(), name='edit_message'),
    path('myforums/', MyForums.as_view(), name='myforums'),
    path('forum/<int:pk>/edit_forum/', EditForum.as_view(), name='edit_forum')
]
