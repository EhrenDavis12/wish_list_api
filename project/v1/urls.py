from django.urls import path, include

urlpatterns = [
    path('app_user/', include('app_user.urls')),
    path('wish_list/', include('project.v1.wish_list.urls')),
    path('app_group/', include('project.v1.app_group.urls')),
]
