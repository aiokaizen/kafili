from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from orphanage.models import Child
from orphanage.resources import ChildResources


class ChildAdmin(ImportExportModelAdmin):
    resource_class = ChildResources

    list_display = ['first_name', 'last_name', 'sex', 'village']
    list_filter = ['sex', 'grade', 'orphan_side', 'chronic_disease']
    search_fields = ['first_name', 'last_name', 'sex', 'village']


admin.site.register(Child, ChildAdmin)
