from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class SalePagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'currentPage'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        print(self.page.paginator.count)
        print(self.page.number)
        return Response({
            'items': data,
            'lastPage': self.page.paginator.count,
            'currentPage': self.page.number,
        })