from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from addresses.views import AddressViewSet
from drivers.views import DriverViewSet
from services.views import ServiceViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'addresses', AddressViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'services', ServiceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
