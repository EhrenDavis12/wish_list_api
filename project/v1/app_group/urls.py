# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.WishListAPI.as_view()),
#     path('<str:pk>/', views.WishListRetrieveUpdateDestroyAPIView.as_view()),
# ]

from django.urls import include, path
from rest_framework import routers
from .views import AppGroupViewSet

router = routers.DefaultRouter()
router.register('', AppGroupViewSet, basename="AppGroup")

urlpatterns = [
    path("", include(router.urls)),
]