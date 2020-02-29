from import_export import resources

from orphanage.models import Child


class ChildResources(resources.ModelResource):

    class Meta:
        model = Child
        skip_unchanged = True
        report_skipped = False

        import_id_fields = ('subscription_id', )

        fields = [
            'subscription_id', 'first_name', 'last_name', 'full_name', 'sex', 'grade', 'birthday', 'phone_number', 'village',
            'weight', 'height', 'bed_position', 'shoo_size', 'vision', 'orphan_side', 'chronic_disease', 'hobby',
            'status', 'full_name'
        ]

        export_order = [
            'subscription_id', 'first_name', 'last_name', 'full_name', 'sex', 'grade', 'birthday', 'phone_number',
            'village', 'weight', 'height', 'bed_position', 'shoo_size', 'vision', 'orphan_side', 'chronic_disease',
            'hobby', 'status'
        ]

    def before_import_row(self, row, **kwargs):
        full_name = row['full_name'].split(' ')
        if len(full_name) == 2:
            row['first_name'] = full_name[0]
            row['last_name'] = full_name[1]
        elif len(full_name) == 3:
            if 'عبد' in full_name:
                row['first_name'] = full_name[0] + ' ' + full_name[1]
                row['last_name'] = full_name[2]
            elif 'ايت' in full_name or 'أيت' in full_name:
                row['first_name'] = full_name[0]
                row['last_name'] = full_name[1] + ' ' + full_name[2]

        if row['sex'] == 'أ':
            row['sex'] = 'f'
        else:
            row['sex'] = 'm'
