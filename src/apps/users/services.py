from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PaginationUsers(PageNumberPagination):
    page_size = 5
    max_page_size = 100
    page_size_query_param = 'count'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'users': data,
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'next': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'http://api.example.org/accounts/?{page_query_param}=4&{page_size_query_param}=30'.format(
                      page_query_param=self.page_query_param, page_size_query_param=self.page_size_query_param
                    )
                },
                'previous': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'http://api.example.org/accounts/?{page_query_param}=2&{page_size_query_param}=30'.format(
                        page_query_param=self.page_query_param, page_size_query_param=self.page_size_query_param
                    )
                },
                'count': {
                    'type': 'integer',
                    'example': 123,
                },
                'users': schema,
            }
        }
