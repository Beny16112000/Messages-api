from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('messages',views.MessagesAll.as_view()),
    path('messages/login',obtain_auth_token),
    path('messages/unread',views.MessagesUnread.as_view()),
    path('messages/<int:id>',views.Messages.as_view()),
]
