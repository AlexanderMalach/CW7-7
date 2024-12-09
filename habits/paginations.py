from rest_framework.pagination import PageNumberPagination


class ViewUserHabitPagination(PageNumberPagination):
    """
    Пагинация при выводе привычек
    """

    page_size = 5
