from django.urls import path

from api.views import HelloView

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
]
