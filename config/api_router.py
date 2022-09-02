from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from geolocations.api.views import LocationViewSet
from sofomo.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()


# router.register("users", UserViewSet)


router.register("locations", LocationViewSet)


app_name = "api"
urlpatterns = router.urls
