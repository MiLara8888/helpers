from django.urls import path
from helpers.views import ControlerViewSet


app_name = 'helpers'

urlpatterns = [
    path('problem/add', ControlerViewSet.as_view({"post":"add_problem"})),  #добавление проблемы
    path('problem/delete/<int:problem_pk>', ControlerViewSet.as_view({"post":"delete_problem"})),    #Изменение на неактивно
    path('problem/update/<int:problem_pk>', ControlerViewSet.as_view({"post":"update_problem"})),    #изменение проблемы
    path('problem/<int:problem_pk>', ControlerViewSet.as_view({"post":"view_problem"})),     #отрисовка страницы проблемы

    path('category/add', ControlerViewSet.as_view({"post":"add_category"})),   #добавление категории
    path('category/delete/<int:category_pk>', ControlerViewSet.as_view({"post":"delete_category"})),    #удаление категории
    path('category/update/<int:category_pk>', ControlerViewSet.as_view({"post":"update_category"})),    #изменение категории

    path('image/delete/<int:image_pk>', ControlerViewSet.as_view({"post":"delete_image"})),    #удаление картинки

    path('category/all', ControlerViewSet.as_view({"post":"all_category"})),     #Вывод всех категорий

    path('problem/category/<int:category_pk>', ControlerViewSet.as_view({"post":"problem_category"})),     #Вывод проблем определённой категории

    path('problem/search', ControlerViewSet.as_view({"post":"search_problem"})),     #поиск

    path("problem/all", ControlerViewSet.as_view({"post":"all_problem"})),
    # path('test/', ControlerViewSet.as_view({"get":"get_test"})),


]



