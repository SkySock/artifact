from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PaginationUsers(PageNumberPagination):
    page_size = 5
    max_page_size = 100
    page_size_query_param = 'count'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'count': self.page.paginator.count,
            'users': data,
        })
