#!/usr/bin/env python
# -- coding: utf-8 --
"""
"""
import json
from datetime import datetime


from django.http.request import HttpRequest
from django.db.transaction import TransactionManagementError
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.db import transaction, DatabaseError, OperationalError, IntegrityError, Error
from django.http import JsonResponse


from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer
# from rest_framework_xml.renderers import XMLRenderer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


from django.core.files.base import ContentFile

from helpers.models import Category, Problem, Media
from helpers.serializers import (SaveProblemSerializer, AddCategorySerializer,
                                 AllCategorySerializer, ProblemCategorySerializer,
                                 ProblemSerializer, SearchSerializer)


import base64


# format, imgstr = data.split(';base64,')
# ext = format.split('/')[-1]

# data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) # You can save this as file instance.

class CatId(Exception):
    pass

class NotField(Exception):
    pass



class ControlerViewSet(ViewSet):
    """ Супер класс преставления """
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, )
    read_only = True



    def error_resp(self, error, message='Ошибка', status=HTTP_400_BAD_REQUEST):
        error_dict = {'error': message}
        # print(error)    #это в логи себе закинуть TODO
        self.resp = JsonResponse(error_dict, status=status)
        self.resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return self.resp

    def decor_error(fn):
        """декоратор отлова ошибок"""
        def wraper(self, *args, **kwargs):
                try:
                    n = fn(self, *args, **kwargs)
                    if n:
                        return Response(n, status=HTTP_201_CREATED)
                    else:
                        return Response(status=HTTP_201_CREATED)

                except TransactionManagementError as e:    # поднимается для любых и всех проблем, связанных с транзакциями базы данных.
                    return self.error_resp(e, 'Ошибка', HTTP_400_BAD_REQUEST)
                except DatabaseError as e:
                    return self.error_resp(e, f'{str(e)} ошибка бд', HTTP_400_BAD_REQUEST)
                except IndexError as e:
                    return self.error_resp(e, f'{str(e)} ошибка бд', HTTP_400_BAD_REQUEST)
                except FieldError as e:    #Исключение FieldError вызывается, если существует проблема с полем модели.
                    return self.error_resp(e, f'{str(e)} ошибка в запрашиваемых полях', status=HTTP_400_BAD_REQUEST )
                except ValidationError as e:
                    return self.error_resp(e, f'Ошибка валидации {str(e)}', HTTP_400_BAD_REQUEST)
                except Error as e:    #Основная для ошибок связанных с бд
                    return self.error_resp(e, f'Ошибка в бд {str(e)}', status=HTTP_400_BAD_REQUEST )
                except NotField as e:
                    return self.error_resp(e, "Поля name, text, html_page, user, category обязательны к заполнению", status=HTTP_400_BAD_REQUEST)
                except AttributeError as e:
                    return self.error_resp(e, f"Ошибка {str(e)}", status=HTTP_400_BAD_REQUEST )
                except ConnectionError  as e:    #Базовый класс для проблем, связанных с подключением.
                    return self.error_resp(e, f'{str(e)} Проблемы с подключением', status=HTTP_400_BAD_REQUEST )
                except RuntimeError as e:
                    return self.error_resp(e, f'{str(e)} Проблемы с подключением', status=HTTP_400_BAD_REQUEST )
                except Exception as e:
                    print(e)
                    return self.error_resp(e, f'{str(e)} Ошибка', status=HTTP_400_BAD_REQUEST )
        return wraper



    @decor_error
    def add_problem(self, request: HttpRequest, *args, **kwargs):
        """ post запрос для добавления ответа"""
        serializer = SaveProblemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                data = serializer.validated_data

                name = data.get('name', '').capitalize()
                text = data.get('text', '')
                html_page = data.get('html_page', '')
                user = data.get('user', 1)
                category = data.get('category', [])

                if name=="" or text=="" or html_page=="" or user=="" or category==[]:
                    raise NotField

                problem = Problem()
                problem.name = name
                problem.text = text
                problem.html_page = html_page
                problem.user = user
                problem.save()

                for i in category:    #добавление категорий
                    problem.category.add(i)

                for i in data.get('problem_media', []):
                    media = Media()
                    media.problem = problem
                    data = i.get("image")
                    format, imgstr = data.split(';base64,')
                    ext = format.split('/')[-1]
                    media.type_file = ext
                    res = ContentFile(base64.b64decode(imgstr), name=f'{problem.id}.{ext}')
                    media.image_path = res
                    media.image = data
                    media.save()
                return


    @decor_error
    def update_problem(self, request: HttpRequest, problem_pk: int, *args, **kwargs):
        """post запрос обновления записи из отображения"""
        serializer = SaveProblemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                data = serializer.validated_data
                problem = Problem.objects.get(pk=problem_pk)

                name = data.get('name', '').capitalize()
                text = data.get('text', '')
                html_page = data.get('html_page', '')
                user = data.get('user', 1)
                category = data.get('category', [])

                problem.name = name
                problem.text = text
                problem.html_page = html_page
                problem.user = user
                problem.save()


                problem.category.clear()

                if name=="" or text=="" or html_page=="" or user=="" or category==[]:
                    raise NotField

                for i in category:
                    problem.category.add(i)

                for i in data.get('problem_media', []):
                    media = Media()
                    media.problem = problem
                    data = i.get("image")
                    format, imgstr = data.split(';base64,')
                    ext = format.split('/')[-1]
                    media.type_file = ext
                    res = ContentFile(base64.b64decode(imgstr), name=f'{problem.id}.{ext}')
                    media.image_path = res
                    media.save()
                return


    @decor_error
    def delete_problem(self, request: HttpRequest, problem_pk: int, *args, **kwargs):
        """post запрос удаления записи из отображения"""
        snippet = Problem.objects.get(pk=problem_pk)
        snippet.is_published = False
        snippet.save()
        return


    @decor_error
    def delete_category(self, request: HttpRequest, category_pk: int, *args, **kwargs):
        """post запрос удаления категории из отображения"""
        snippet = Category.objects.get(pk=category_pk)
        for i in snippet.problem_set.all():
            if i.category.count()==1:
                i.is_published=False
                i.save()
        snippet.delete()
        return


    @decor_error
    def delete_image(self, request: HttpRequest, image_pk: int, *args, **kwargs):
        """post запрос удаления картинки из отображения"""
        snippet = Media.objects.get(pk=image_pk)
        snippet.delete()
        return


    @decor_error
    def add_category(self, request: HttpRequest, *args, **kwargs):
        """post добавление категории"""
        serializer = AddCategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            try:
                cat = Category.objects.get(cat_name=data.get("cat_name"))
            except Category.DoesNotExist as e:
                cat = Category()
                cat.cat_name = data.get("cat_name").capitalize()
                cat.save()
            return cat.id


    @decor_error
    def update_category(self, request: HttpRequest, category_pk: int, *args, **kwargs):
        serializer = AddCategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            cat = Category.objects.get(pk=category_pk)
            cat.cat_name = data.get("cat_name", "").capitalize()
            cat.save()
            return



    # @decor_error      #с пагинацией
    # def all_category(self, request: HttpRequest, *args, **kwargs):
    #     records = Category.objects.all().order_by('cat_name')
    #     pagination = PageNumberPagination()
    #     qs = pagination.paginate_queryset(records, request)
    #     serializer = AllCategorySerializer(qs, many=True)
    #     return pagination.get_paginated_response(serializer.data).data

    @decor_error
    def all_category(self, request: HttpRequest, *args, **kwargs):
        records = Category.objects.all().order_by('cat_name')
        serializer = AllCategorySerializer(records, many=True)
        return serializer.data




#path('problem/category/<int:category_pk>', ControlerViewSet.as_view({"post":"problem_category"})),     #Вывод проблем определённой категории


    @decor_error
    def problem_category(self, request: HttpRequest, category_pk: int, *args, **kwargs):
        """проблемы категории с пагинацией"""
        problem = Problem.objects.all().order_by('-time_update').filter(category=category_pk, is_published=True)
        pagination = PageNumberPagination()
        qs = pagination.paginate_queryset(problem, request)
        serializer = ProblemCategorySerializer(qs, many=True)
        return pagination.get_paginated_response(serializer.data).data


    @decor_error
    def view_problem(self, request: HttpRequest, problem_pk: int, *args, **kwargs):
        problem = Problem.objects.get(pk=problem_pk)
        if problem.is_published == True:
            serializer = ProblemSerializer(problem, many=False)
            return serializer.data
        raise FieldError



    @decor_error
    def all_problem(self, request: HttpRequest, *args, **kwargs):
        problem = Problem.objects.all()
        serializer = ProblemCategorySerializer(problem, many=True)
        return serializer.data



    @decor_error
    def search_problem(self, request: HttpRequest, *args, **kwargs):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            search_text = data.get("search", "")

            records = Problem.objects.raw(f"""select hp.*
                                                from helpers_problem hp
                                                where to_tsvector('russian', "name") || to_tsvector('russian', "text") @@  plainto_tsquery('{search_text}')
                                                ORDER BY ts_rank(to_tsvector('russian', "text"), plainto_tsquery('{search_text}')), ts_rank(to_tsvector('russian', "name"), plainto_tsquery('{search_text}')), time_create desc;""")
            pagination = PageNumberPagination()
            qs = pagination.paginate_queryset(records, request)
            serializer = ProblemCategorySerializer(qs, many=True)
            return pagination.get_paginated_response(serializer.data).data
