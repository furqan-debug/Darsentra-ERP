from django.urls import path

from .views import SchoolDetailView, UserMembershipsListView, UserSchoolsListView

app_name = "schools"

urlpatterns = [
    path("", UserSchoolsListView.as_view(), name="school_list"),
    path("memberships/", UserMembershipsListView.as_view(), name="user_memberships"),
    path("<uuid:school_id>/", SchoolDetailView.as_view(), name="school_detail"),
]
