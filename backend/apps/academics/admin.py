from django.contrib import admin

from .models import AcademicClass, AcademicYear, ClassSubject, Section, Subject


class SectionInline(admin.TabularInline):
    model = Section
    extra = 1


class ClassSubjectInline(admin.TabularInline):
    model = ClassSubject
    extra = 1


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("name", "school", "start_date", "end_date", "is_current")
    list_filter = ("school", "is_current")
    search_fields = ("name", "school__name")


@admin.register(AcademicClass)
class AcademicClassAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "school", "order")
    list_filter = ("school",)
    search_fields = ("name", "code", "school__name")
    inlines = [SectionInline, ClassSubjectInline]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("name", "academic_class", "school", "room_number", "capacity")
    list_filter = ("school", "academic_class")
    search_fields = ("name", "academic_class__name", "school__name")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "school", "is_elective")
    list_filter = ("school", "is_elective")
    search_fields = ("name", "code", "school__name")
