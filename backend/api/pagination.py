from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from .constants import PAGE_SIZE

class CustomPagination(PageNumberPagination):
    """Настройка пагинации."""

    page_query_param = 'page'
    page_size_query_param = 'limit'
    max_page_size = PAGE_SIZE