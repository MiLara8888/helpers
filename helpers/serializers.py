#!/usr/bin/env python
# -- coding: utf-8 --
"""
сериализация объектов
"""
from rest_framework import serializers
from helpers.models import Category, Problem, Media


# Category: "cat_name", "cat_time_create"
# Problem: "user", "name", "text", "html_page", "time_create", "time_update", "category", "is_published"
# Media: "problem", "image", "image_path"



class SaveProblemSerializer(serializers.ModelSerializer):
    """ для добавления проблемы"""

    # problem_media = MediaSerializer(read_only=True, many=True)
    problem_media = serializers.ListField()

    # problem_media = serializers.PrimaryKeyRelatedField(many=True, read_only=True)     #это даст мне айдишники

    class Meta:
        model = Problem
        fields = ("user", "name", "text", "html_page", "category", "problem_media")


class SearchSerializer(serializers.ModelSerializer):
    search = serializers.CharField()
    class Meta:
        model = Problem
        fields = ("search",)


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ("id", "problem", "image", "image_path")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "cat_name", "cat_time_create")

class ProblemSerializer(serializers.ModelSerializer):
    problem_media = MediaSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Problem
        fields = ("id", "user", "name", "text", "html_page", "time_create", "time_update", "problem_media", "category")



class ProblemCategorySerializer(serializers.ModelSerializer):    #TODO что выводить???

    class Meta:
        model = Problem
        fields = ("id", "user", "name", "text", "html_page", "time_create", "time_update", "category")



class AddCategorySerializer(serializers.ModelSerializer):

    cat_name = serializers.CharField()
    class Meta:
        model = Category
        fields = ("cat_name", )



class AllCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("cat_name", "id" )


