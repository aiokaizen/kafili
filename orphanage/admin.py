from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from orphanage.models import Child, Student, Year, Grade, Subject, Mark, Guardian
from orphanage.resources import ChildResources


@admin.register(Child)
class ChildAdmin(ImportExportModelAdmin):
    resource_class = ChildResources

    list_display = ['first_name', 'last_name', 'village']
    list_filter = ['sex', 'orphan_side', 'chronic_disease']
    search_fields = ['first_name', 'last_name', 'village']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['child', 'grade']
    list_filter = ['grade']
    search_fields = ['child__first_name', 'child__last_name']


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    pass


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    pass


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    pass
