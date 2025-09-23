from django.urls import path
from classes.views import (
    ClassCreateView,
    ClassDeleteView,
    ClassListBySchoolView,
    ClassRetrieveView,
    ClassListView,
    ClassUpdateView,
)

urlpatterns = [
    path("create/", ClassCreateView.as_view(), name="class-create"),
    path("list/", ClassListView.as_view(), name="class-list"),
    path("retrieve/<int:pk>/", ClassRetrieveView.as_view(), name="class-retrieve"),
    path("update/<int:pk>/", ClassUpdateView.as_view(), name="class-update"),
    path("delete/<int:pk>/", ClassDeleteView.as_view(), name="class-delete"),
    path(
        "list-by-school/", ClassListBySchoolView.as_view(), name="class-list-by-school"
    ),  
]
