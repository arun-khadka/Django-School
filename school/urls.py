from django.urls import path
from school.views import SchoolCreateView, SchoolListView

urlpatterns = [
    path("create/", SchoolCreateView.as_view(), name="school-create"),
    path("list/", SchoolListView.as_view(), name="school-list"),

]
