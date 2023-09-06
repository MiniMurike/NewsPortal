from django.urls import path, include
from .views import subscriptions

urlpatterns = [
    path('', subscriptions, name='subscriptions'),
]
