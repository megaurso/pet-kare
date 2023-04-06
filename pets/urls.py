from django.urls import path
from .views import PetView,PetInfoView

urlpatterns = [
    path("pets/", PetView.as_view()),
    path("pets/<int:pet_id>/", PetInfoView.as_view())             
               
]
