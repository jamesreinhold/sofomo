import contextlib

from django.contrib.auth import get_user_model
from django.http.response import Http404
from django.utils.translation import gettext_lazy as _
from ipware.ip import get_client_ip
from rest_framework import generics, status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from geolocations.models import Location
from geolocations.utils import get_geolocation_data

from .serializers import LocationSerializer

User = get_user_model()


class LocationViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet):
    """
    Create a Location (JSON)

    This endpoint allows you to create a new location by passing IP as body
    """
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    lookup_field = "ip_address"
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get_object(self, queryset=None):
        return Location.objects.filter(pk=self.kwargs['ip_address']).first()

    def list(self, request, *args, **kwargs):
        """
        List Location

        This endpoints returns list of all locations
        """
        return super(LocationViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Get an Location

        Retrieve details of an Location by passed Id.
        """
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({'message': str(e)})
        else:
            # any additional logic
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an Location

        This endpoints allows you to delete an Location by passed Id.
        """
        with contextlib.suppress(Http404):
            instance = self.get_object()
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddLocationResponse(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = LocationSerializer


    def get(self, request, ip_address, *args, **kwargs):
        """
        Add a new location - Manual

        This endpoint allows you to add a new location by passed IP address manually

        ## 1 When wrong IP address is provided:

        **Example Response**:

                {
                    "success": false,
                    "error": {
                        "code": 106,
                        "type": "invalid_ip_address",
                        "info": "The IP Address supplied is invalid."
                    }
                }
        """
        ipstack_data = get_geolocation_data(ip_address)
        if 'success' in ipstack_data:
            return Response(ipstack_data, status=status.HTTP_400_BAD_REQUEST)
        if location_exist := Location.objects.filter(ip=ip_address).exists():
            # location = Location.objects.get(ip=ip_address)
            serializer = LocationSerializer(Location.objects.get(ip=ip_address))
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # location does not exist
        location = Location.objects.create(**ipstack_data)
        serializer = LocationSerializer(location)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class AutomaticAddLocationResponse(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    serializer_class = LocationSerializer

    def get(self, request, *args, **kwargs):
        """
        Add a new location - (Automatic)

        This endpoint allows you to add a new location by passed IP address automatically.
        """
        client_ip, is_routable = get_client_ip(request)
        if location_exist := Location.objects.filter(ip=client_ip).exists():
            location = Location.objects.get(ip=client_ip)
            serializer = LocationSerializer(location)
            return Response(serializer.data)
        
        # location does not exist
        location = Location.objects.create(**get_geolocation_data(client_ip))
        serializer = LocationSerializer(location)
        return Response(serializer.data)
