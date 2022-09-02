import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

from geolocations.utils import get_geolocation_data

from ..models import Location

logger = logging.getLogger(__name__)

class LocationSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    ip = serializers.IPAddressField(
        label=_("IP Address"),
        help_text=_("The IP Address of the user at the time of creating record.")
    )
    
    class Meta:
        model = Location
        fields = "__all__"
    
    def validate_ip(self, value):
        if ip_exists := Location.objects.filter(ip=value).exists():
            self.register_error(
                error_message="IP address already exist in database",
                error_code="ip_already_exsit",
                field_name="ip"
            )
        
        return value
    
    def create(self, validated_data):
        logger.info(f"{__name__}: Creating a record...")
        ipstack_data = get_geolocation_data(validated_data['ip'])
        if 'success' in ipstack_data:
            return Response(ipstack_data, status=status.HTTP_400_BAD_REQUEST)
        return super().create(ipstack_data)
