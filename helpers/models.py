#!/usr/bin/env python
# -- coding: utf-8 --
"""
# Category: "cat_name", "cat_time_create"
# Problem: "user", "name", "text", "html_page", "time_create", "time_update", "category", "is_published"
# Media: "problem", "image", "image_path"

"""
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver




class Category(models.Model):
    """модель с категориями"""
    cat_name = models.CharField(max_length=150, unique=True, verbose_name="наименование")
    cat_time_create = models.DateTimeField(auto_now_add=True, verbose_name="время создания")


    def __str__(self):
        return self.cat_name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Problem(models.Model):
    """модель с проблемами """
    user = models.IntegerField( verbose_name="юзер id")
    # url = models.CharField(max_length=600, blank=True, null=True, verbose_name="url страницы")
    name = models.CharField(max_length=300, verbose_name="заголовок проблемы")
    text = models.TextField(blank=True, verbose_name="текст проблемы")
    html_page = models.TextField(blank=True, verbose_name="html страницы")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="время изменения")
    category = models.ManyToManyField(Category, blank=True, verbose_name = 'Категории')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Проблема"
        verbose_name_plural = "Проблемы"


def my_directory(instance, filename):

    return 'media/problem_{0}/image/{1}'.format(instance.problem.id, filename)




class Media(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, verbose_name="проблема", related_name='problem_media')
    image = models.TextField(blank=True, null=True, verbose_name='base64 картинки')
    image_path = models.FileField(upload_to=my_directory, verbose_name='путь хранения картинки')
    type_file = models.CharField(max_length=30, blank=True, null=True, verbose_name="тип файла")


    class Meta:
        verbose_name = "Картинки"
        verbose_name_plural = "Картинки"

@receiver(pre_delete, sender=Media)
def image_model_delete(sender, instance, **kwargs):
    if instance.image_path.name:
        instance.image_path.delete(False)