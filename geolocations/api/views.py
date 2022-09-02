import contextlib

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http.response import Http404
from django.utils.translation import gettext_lazy as _
from pyrsistent import v
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
from .serializers import LocationSerializer


User = get_user_model()


class LocationViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    lookup_field = "id"
    lookup_value_regex = '[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}'
    permission_classes = [IsAuthenticated]

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