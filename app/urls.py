from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('',views.MessagesAll, basename='messages')

urlpatterns = [
    path('messages/login',obtain_auth_token),
    path('messages/',include(router.urls)),
    path('messages/unread', views.MessagesAll.as_view({'get': 'unreadMessages'}))
]
