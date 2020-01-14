from import_export import resources
from import_export.fields import Field

from orphanage.models import Child


class ChildResources(resources.ModelResource):

    full_name = Field(column_name='full_name')

    class Meta:
        model = Child
        skip_unchanged = True
        report_skipped = False
        fields = [
            'full_name', 'first_name', 'last_name', 'sex', 'grade', 'birthday', 'phone_number', 'village', 'weight', 'height',
            'bed_position', 'shoo_size', 'vision', 'orphan_side', 'chronic_disease', 'hobby', 'status'
        ]
        export_order = [
            'first_name', 'last_name', 'full_name', 'sex', 'grade', 'birthday', 'phone_number', 'village', 'weight', 'height',
            'bed_position', 'shoo_size', 'vision', 'orphan_side', 'chronic_disease', 'hobby', 'status'
        ]

    def before_import_row(self, row, **kwargs):
        full_name = row['full_name'].split(' ')
        if len(full_name) == 2:
            row['first_name'] = full_name[0]
            row['last_name'] = full_name[1]
        else:
            row['first_name'] = '? ' + row['full_name']

        if row['sex'] == 'أ':
            row['sex'] = 'f'
        else:
            row['sex'] = 'm'
