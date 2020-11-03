from django.urls import reverse
from django.contrib.auth.models import *

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

STATUS_CHOICES = (
    ('active', 'Активен'),
    ('warn', 'Вынесено предупреждение'),
    ('block', 'Заблокирован'),
    ('delate', 'Удален'),
)


class Users(AbstractUser):
    age = models.DateField(blank=True, null=True, verbose_name='Дата Рождения', )
    photo = models.ImageField(blank=True, upload_to='userphotos/', verbose_name='Фото')
    status = models.CharField(max_length=150, choices=STATUS_CHOICES, default='active', verbose_name='Статус')

    def get_absolute_url(self):
        """
        Get user address
        :return: url of the selected user
        """
        return reverse('user', kwargs={"username": self.username})

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, unique=True, verbose_name='Название категории')
    commit = models.TextField(max_length=1000, verbose_name='Описание категории')

    def get_absolute_url(self):
        """
        Get category address
        :return: url of the selected category
        """
        return reverse('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Котегория'
        verbose_name_plural = 'Категории'
        ordering = ['pk']


class Forum(models.Model):
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True,
                                 verbose_name='Категория')
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    commit = RichTextField(blank=False, verbose_name='Описание')
    logo = models.ImageField(blank=True, upload_to='forumlogos/', verbose_name='Логотип')
    creator = models.ForeignKey('Users', on_delete=models.PROTECT, null=True, verbose_name='Создатель')
    is_published = models.BooleanField(default=True,
                                       verbose_name='Публичность')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def get_absolute_url(self):
        """
        Get forum address
        :return: url of the selected forum
        """
        return reverse('forum', kwargs={"forum_id": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Форум'
        verbose_name_plural = 'Форумы'
        ordering = ['-create_date']


class Message(models.Model):
    id_forum = models.ForeignKey('Forum', on_delete=models.CASCADE, null=True,
                                 verbose_name='Форум')
    id_user = models.ForeignKey('Users', on_delete=models.PROTECT, null=True,
                                verbose_name='Пользователь')
    text = RichTextField(blank=False, verbose_name='Сообщение')
    create_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        """
        Get message address
        :return: url of the selected message
        """
        return reverse('message', kwargs={"message_id": self.pk})

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['create_date']

    def __str__(self):
        return self.text


class File(models.Model):
    id_user = models.IntegerField()
    file = models.FileField(
        upload_to=f'files/{id_user}')
    is_published = models.BooleanField(default=True)
    add_date = models.DateTimeField(auto_now_add=True)
