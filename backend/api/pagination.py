from rest_framework.pagination import PageNumberPagination

from .constants import PAGE_SIZE

class CustomPagination(PageNumberPagination):
    """Настройка пагинации."""

    page_query_param = 'page'
    page_size_query_param = 'limit'
    max_page_size = PAGE_SIZE