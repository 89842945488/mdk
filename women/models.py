from django.db import models
from .models import *
from django.urls import reverse
# Create your models here.

# чтобы у нас в БД появилась таблица
#  с такой структурой нам достаточно
#  объявить класс с этими полями, а
# затем, выполнить миграцию. Сначала
# определим класс модели. Для этого
#  перейдем в файл women/models.py, в
# котором принято описывать все модели
#  текущего приложения. И здесь вначале
#  уже импортирован пакет models,
# содержащий базовый класс Model, на базе
# которого и строятся модели


class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(
        auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey(
        'Category', on_delete=models.PROTECT, verbose_name="Категории")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Арты и биографии'
        verbose_name_plural = 'Арты и биографии'
        ordering = ['time_create', 'title']


class Category(models.Model):
    name = models.CharField(
        max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name  # В результате, в таблице category будет два индексируемых поля: id и name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
