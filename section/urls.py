from django.urls import path
from section.views import (
    SectionCreateView,
    SectionListByClassView,
    SectionListBySchoolClassView,
    SectionListAllView,  # new view to list all sections with classes
)

urlpatterns = [
    path("create/", SectionCreateView.as_view(), name="section-create"),
    
    # Fetch sections by school & class
    path(
        "sections/<int:school_id>/<int:class_id>/",
        SectionListByClassView.as_view(),
        name="sections-by-class",
    ),
    
    path(
        "list-by-school-class/<int:school_id>/<int:class_id>/",
        SectionListBySchoolClassView.as_view(),
        name="section-list-by-school-class",
    ),

    # New endpoint: fetch all sections with their respective classes
    path(
        "all/",
        SectionListAllView.as_view(),
        name="sections-all",
    ),
]
