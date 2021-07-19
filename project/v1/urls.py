from django.urls import path, include

urlpatterns = [
    path('user/', include('project.v1.user.urls')),
    path('wishlist/', include('project.v1.wish_list.urls')),
]
