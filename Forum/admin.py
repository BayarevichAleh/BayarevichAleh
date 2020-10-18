from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from .models import *

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'age', 'status')
    list_display_links = ['username']
    fields = ('groups', 'username', 'password', 'email', 'first_name', 'last_name', 'age', 'photo', 'status')
    search_fields = ('username', 'first_name', 'last_name')
    list_editable = ('status',)
    list_filter = ('status',)


class ForumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'creator', 'create_date')
    list_display_links = ['name']
    search_fields = ('name', 'creator')
    list_editable = ('category',)
    list_filter = ('category',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ['title']


class MessageFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Message
        fields = '__all__'


class MessageAdmin(admin.ModelAdmin):
    form = MessageFormAdmin
    list_display = ('id', 'id_user', 'id_forum', 'text', 'create_date')
    list_display_links = ['id', 'id_user', 'id_forum']
    search_fields = ('id', 'id_user', 'id_forum')


admin.site.register(Users, UsersAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Message, MessageAdmin)
