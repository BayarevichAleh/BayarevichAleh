from django.db import models
from django.urls import reverse


# Create your models here.


class User(models.Model):
    """
    Модель хранения данных пользователей
    """
    group_choices = (
        ('admin', 'Администратор'),
        ('user', 'Пользователь'),
    )
    status_choices = (
        ('active', 'Активен'),
        ('warn', 'Вынесено предупреждение'),
        ('block', 'Заблокирован'),
        ('delate', 'Удален'),
    )
    group = models.CharField(max_length=150, choices=group_choices, default='user', verbose_name='Группа')
    login = models.CharField(max_length=50, verbose_name='Логин', unique=True)  # Логин юзера
    password = models.CharField(max_length=100, verbose_name='Пароль')  # Его пароль
    email = models.EmailField(max_length=50, verbose_name='E-mail')  # E-mail юзера
    name = models.CharField(max_length=50, verbose_name='Имя')  # Имя юзера
    lastname = models.CharField(blank=True, max_length=100, verbose_name='Фамиллия')  # Фамилия юзера (не обязательное)
    age = models.DateField(blank=True, verbose_name='Дата Рождения')  # Возраст юзера
    photo = models.ImageField(blank=True, upload_to='userphotos/', verbose_name='Фото')  # Фото юзера
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')  # Дата регистрации
    status = models.CharField(max_length=150, choices=status_choices, default='active', verbose_name='Статус')

    def __str__(self):
        return self.login

    # def get_absolute_url(self):
    #     return reverse('index')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['login']



class Category(models.Model):
    """
    Модель категорий форумов
    """
    title = models.CharField(max_length=150, db_index=True, verbose_name='Название категории')  # Название категории
    commit = models.TextField(max_length=1000, verbose_name='Описание категории')  # Краткое описание категории

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Котегория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Forum(models.Model):
    """
    Модель форумов
    """
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True,
                                 verbose_name='Категория')  # id категории форумов
    name = models.CharField(max_length=100, verbose_name='Название')  # Название форума
    commit = models.TextField(verbose_name='Описание')  # Краткое описание форума
    logo = models.ImageField(blank=True, upload_to='forumlogos/', verbose_name='Логотип')  # логотип форума
    creator = models.ForeignKey('User', on_delete=models.PROTECT, null=True, verbose_name='Создатель')  # id создателя
    # id_admin = models.IntegerField(blank=True, verbose_name='')  # id администраторов
    # id_moderator = models.IntegerField(blank=True)  # id модераторов
    # id_user = models.IntegerField(blank=True)  # id пользователей для которых открыт форум
    is_pablished = models.BooleanField(default=True,
                                       verbose_name='Публичность')  # Флаг публичности форума, по умолчанию доступен всем
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  # Дата создания форума

    def get_absolute_url(self):
        return reverse('forum', kwargs={"forum_id": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Форум'
        verbose_name_plural = 'Форумы'
        ordering = ['name']


class Message(models.Model):
    """
    Модель сообщений
    """
    id_forum = models.ForeignKey('Forum', on_delete=models.CASCADE, null=True,
                                 verbose_name='Форум')  # id форума к которому пренадлежит сообщение
    id_user = models.ForeignKey('User', on_delete=models.PROTECT, null=True,
                                verbose_name='Пользователь')  # id юзера создавшего сообщение
    text = models.TextField()  # Содержание сообщения
    create_date = models.DateTimeField(auto_now_add=True)  # Дата создания сообщения

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['create_date']

    def __str__(self):
        return self.text


class File(models.Model):
    """
    Модель файлов
    """
    id_user = models.IntegerField()  # id юзера кому пренадлежит файл
    file = models.FileField(
        upload_to=f'files/{id_user}')  # Ссылка на файл (файлы должны храниться в облачных храниллищах или файлообменниках)
    is_published = models.BooleanField(default=True)  # Публичный доступ
    add_date = models.DateTimeField(auto_now_add=True)  # Дата добавления
