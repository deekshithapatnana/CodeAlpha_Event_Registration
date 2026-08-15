from django.urls import path
from .views import (
    event_list,
    register_participant,
    registration_list,
    cancel_registration
)

urlpatterns = [
    path('events/', event_list),
    path('register/', register_participant),
    path('registrations/', registration_list),
    path(
        'registrations/<int:registration_id>/cancel/',
        cancel_registration
    ),
]