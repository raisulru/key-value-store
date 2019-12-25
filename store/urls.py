from django.urls import path
from .views import KeyValueApiView

urlpatterns = [
    path('values', KeyValueApiView.as_view(), name='key-value-api')
]