from django.urls import path

from .views import (
    ActiveSchoolView,
    SchoolDetailView,
    SchoolSetupView,
    UserMembershipsListView,
    UserSchoolsListView,
)

app_name = "schools"

urlpatterns = [
    path("", UserSchoolsListView.as_view(), name="school_list"),
    path("setup/", SchoolSetupView.as_view(), name="school_setup"),
    path("active/", ActiveSchoolView.as_view(), name="active_school"),
    path("memberships/", UserMembershipsListView.as_view(), name="user_memberships"),
    path("<uuid:school_id>/", SchoolDetailView.as_view(), name="school_detail"),
]
