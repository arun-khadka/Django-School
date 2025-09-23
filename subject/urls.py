from django.urls import path
from subject.views import SubjectCreateView, SubjectListByUserView, SubjectListView, SubjectDeleteView

urlpatterns = [
    path("create/", SubjectCreateView.as_view(), name="subject-create"),
    path("list/<int:class_id>/", SubjectListView.as_view(), name="subject-list"),
    # Get subjects of a specific section in a class
    path(
        "list/<int:class_id>/<str:section_name>/",
        SubjectListView.as_view(),
        name="subject-list-section",
    ),
    path("delete/<int:pk>/", SubjectDeleteView.as_view(), name="subject-delete"),
    path("all/", SubjectListByUserView.as_view(), name="subjects-all"),

]
