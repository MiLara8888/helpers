#!/usr/bin/env python
# -- coding: utf-8 --
"""

"""
from django.contrib import admin
from helpers.models import Category, Media, Problem
from django.db import models


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_name', 'cat_time_create')    #отображение в списке
    fields = ('cat_name', 'cat_time_create')
    readonly_fields = ('cat_time_create',)



@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    # 'user', 'name', 'description', 'time_create', 'completion_date', 'state', 'priority', 'project'
    list_display = ('problem', 'image_path')    #отображение в списке
    fields = ('problem', 'image', 'image_path')


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    # raw_id_fields = ['name']
    list_display = ('name', 'is_published',)

    list_filter = ('category',)       #фильтрация
    fields = ('user', 'name', 'text', 'html_page', 'category', 'is_published',)    #указывать явно если нужна определенная последовательность или явно нужны ОПРЕДЕЛЕННЫЕ ПОЛЯ



admin.site.site_header = ('Админ-панель f.a.q.')
admin.site.site_title = ('Админ-панель f.a.q.')
admin.site.empty_value_display = '(None)'