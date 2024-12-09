from rest_framework.pagination import PageNumberPagination
from django.utils.translation import gettext_lazy as _


class ViewUserHabitPagination(PageNumberPagination):
    """
    Пагинация при выводе привычек
    """
    page_size = 5
    page_size_query_param = "page_size"  # Пользователь может задать ?page_size=10
    max_page_size = 50  # Максимум 50 объектов на странице
    page_query_param = "p"  # Параметр страницы, например, ?p=2
