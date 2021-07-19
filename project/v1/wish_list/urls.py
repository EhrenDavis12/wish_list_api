# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.WishListAPI.as_view()),
#     path('<str:pk>/', views.WishListRetrieveUpdateDestroyAPIView.as_view()),
# ]

from django.urls import include, path
from rest_framework import routers
from .views import WishListViewSet

router = routers.DefaultRouter()
router.register('', WishListViewSet, basename="WishList")

urlpatterns = [
    path("", include(router.urls)),
]