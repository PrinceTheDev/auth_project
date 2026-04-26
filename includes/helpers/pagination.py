from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response



class APIPagination(PageNumberPagination):

    page_size = 10 # set default page size
    page_size_query_param = 'page_size' # allow clients to set page size using query parameter
    max_page_size = 100 # set maximum page size to prevent abuse

    def get_paginated_response(self, data):
        """
        This function generates a paginated response with optional page number and ellipse.

        It returns a Response object with paginated data.
        """
        return Response(
            OrderedDict(
                [
                    ('count', self.page.paginator.count),
                    ('page', self.page.paginator.number),
                    ('page_size', self.page.paginator.per_page),
                    ('total_pages', self.page.paginator.num_pages),
                    ('next', self.get_next_link()),
                    ('next_page_number', self.__get_next_page_number()),
                    ('previous', self.get_previous_link()),
                    ('previous_page_number', self.__get_previous_page_number()),
                    ('ellipse', self.__get_ellipse()),
                    ('results', data)
                ]
            )
        )
    

    def __get_next_page_number(self):
        return self.page.next_page_number() if self.page.has_next() else None
    
    def __get_previous_page_number(self):
        return self.page.previous_page_number() if self.page.has_previous() else None

    def __get_ellipse(self, display_count=5):
        current_page = self.page.number
        total_pages = self.page.paginator.num_pages

        if total_pages <= display_count:
            return list(range(1, total_pages + 1))
        
        start_range = max(1, current_page - (display_count // 2))
        end_range = min(total_pages, start_range + display_count - 1)

        
        if end_range - start_range + 1 < display_count:
            start_range = max(1, end_range - display_count + 1)
        if end_range - start_range + 1 < display_count:
            end_range = min(total_pages, start_range + display_count - 1)


        page_range = []
        if start_range > 1:
            page_range.append(1)
            if start_range > 2:
                page_range.append(None)


        page_range.extend(range(start_range, end_range + 1))

        if end_range < total_pages:
            if end_range < total_pages - 1:
                page_range.append(None)
            page_range.append(total_pages)

        return page_range


    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "example": 123,
                },
                "page": {"type": "integer", "example": 1},
                "page_size": {"type": "integer", "example": 10},
                "total_pages": {"type": "integer", "example": 123},
                "next": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.org/accounts/?{page_query_param}=4".format(
                        page_query_param=self.page_query_param
                    ),
                },
                "next_page_number": {"type": "integer", "nullable": True, "example": 4},
                "previous": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.org/accounts/?{page_query_param}=2".format(
                        page_query_param=self.page_query_param
                    ),
                },
                "previous_page_number": {
                    "type": "integer",
                    "nullable": True,
                    "example": 2,
                },
                "ellipse": {
                    "type": "array",
                    "items": {"type": "integer", "example": 3},
                    "example": [1, 2, 3, 4, 5],
                },
                "results": schema,
            },
        }