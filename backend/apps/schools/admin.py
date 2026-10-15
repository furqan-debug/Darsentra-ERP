from django.contrib import admin

from .models import School, SchoolMembership


class SchoolMembershipInline(admin.TabularInline):
    model = SchoolMembership
    extra = 1
    fields = ("user", "role", "is_active")
    raw_id_fields = ("user",)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "slug",
        "curriculum_type",
        "city",
        "province",
        "is_active",
        "created_at",
    )
    list_filter = ("curriculum_type", "province", "is_active")
    search_fields = ("name", "code", "slug", "registration_number", "city")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SchoolMembershipInline]


@admin.register(SchoolMembership)
class SchoolMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "school", "role", "is_active", "created_at")
    list_filter = ("role", "is_active", "school")
    search_fields = ("user__email", "user__first_name", "user__last_name", "school__name", "school__code")
    raw_id_fields = ("user", "school")
