from django.contrib import admin

from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'login', 'name', 'lastname', 'registration_date', 'group', 'status')
    list_display_links = ['login']
    search_fields = ('login', 'name', 'lastname')
    list_editable = ('group', 'status')
    list_filter = ('group', 'status')

class ForumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'creator', 'create_date')
    list_display_links = ['name']
    search_fields = ('name','creator')
    list_editable = ('category',)
    list_filter = ('category',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ['title']

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_user', 'id_forum', 'text', 'create_date')
    list_display_links = ['id', 'id_user', 'id_forum']
    search_fields = ('id', 'id_user', 'id_forum')


admin.site.register(User,UserAdmin)
admin.site.register(Forum,ForumAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Message,MessageAdmin)