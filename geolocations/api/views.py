import contextlib

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http.response import Http404
from django.utils.translation import gettext_lazy as _
from rest_framework import filters, generics, status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from geolocations.models import Location
from geolocations.utils import get_geolocation_data
from rest_framework.views import APIView


from .serializers import LocationSerializer

User = get_user_model()


class LocationViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    lookup_field = "ip_address"
    permission_classes = [IsAuthenticated]

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


class AddLocationResponse(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LocationSerializer

    def get(self, request, ip_address, *args, **kwargs):
        """
        Add a new location

        This endpoint allows you to add a new location by passed IP address
        """
        if location_exist := Location.objects.filter(ip=ip_address).exists():
            location = Location.objects.get(ip=ip_address)
            serializer = LocationSerializer(location)
            return Response(serializer.data)
        
        # location does not exist
        location = Location.objects.create(**get_geolocation_data(ip_address))
        serializer = LocationSerializer(location)
        return Response(serializer.data)
