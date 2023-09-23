from django.conf import settings
from django.urls import path
from django.urls import include
from rest_framework import routers

from knox.views import LogoutView

from . import views

__all__ = ['urlpatterns', ]

router = routers.DefaultRouter(trailing_slash=settings.APPEND_SLASH, )
# router.register(r'user', views.UserViewSet, basename='user', )
router.register(r'reservation', views.ReservationViewSet, basename='reservation', )

urlpatterns = [
    # path('login', views.UserLoginView.as_view(), name='login'),
    # path('logout', LogoutView.as_view(), name='logout'),
] + router.urls
