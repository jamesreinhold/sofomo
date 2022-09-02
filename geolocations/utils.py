import requests
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

API_KEY = settings.IPSTACK_API_KEY


def get_geolocation_data(ip_address:str="37.30.100.73")->dict:
    """
    Get location data by IP address

    Args:
        ip_address (str, optional): The IP address. Defaults to "37.30.100.73".

    Returns:
        dict: Geolcation data from IP Stack
    """
    url = f"http://api.ipstack.com/{ip_address}?access_key={API_KEY}"
    
    return requests.get(url).json()
    # if response.status_code == 200:
    #     response.json()
    # return "Error"
    



class ContentRangeHeaderPagination(PageNumberPagination):
    """
    A custom Pagination class to include Content-Range header in the
    response.
    """

    def get_paginated_response(self, data):
        """
        Override this method to include Content-Range header in the response.

        For eg.:
        Sample Content-Range header value received in the response for
        items 11-20 out of total 50:

                Content-Range: items 10-19/50
        """

        total_items = self.page.paginator.count  # total no of items in queryset
        item_starting_index = self.page.start_index() - 1  # In a page, indexing starts from 1
        item_ending_index = self.page.end_index() - 1

        content_range = 'items {0}-{1}/{2}'.format(item_starting_index, item_ending_index, total_items)

        headers = {'Content-Range': content_range}

        return Response(data, headers=headers)
