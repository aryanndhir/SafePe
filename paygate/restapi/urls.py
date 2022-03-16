from django.urls import path
from paygate.restapi.views import transact


urlpatterns = [
    path('', transact, name="transaction"),
]