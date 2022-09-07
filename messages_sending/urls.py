from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.ProfileViewSet)
router.register(r'messages', views.MessageViewSet)
urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api/message-per-user-id/', views.message_per_user, name='message-per-user-id'),
    path('api/message-unread-per-user-id/', views.message_unread_per_user,
         name='message-unread-per-user-id'),
    path('api/read-message/<str:message_id>', views.read_message,
         name='read-message'),
    path('api/delete-message/<str:message_id>', views.delete_message,
         name='delete-message'),
    path('api/create-message/', views.create_message,
         name='create-message'),
    path('api/login/', views.login_method,
         name='login'),

]
