from rest_framework import serializers
from geolocations.utils import get_geolocation_data
from ..models import Location



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
    
    def create(self, validated_data):
        
        return super().create(validated_data)
