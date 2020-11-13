from import_export import resources

from orphanage.models import Child, Year, Grade, Student


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
            'subscription_id', 'first_name', 'last_name', 'full_name', 'sex', 'birthday', 'phone_number',
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
            
        status = row['status']
        if status == 'وافد':
            row['status'] = 'new'
        elif status == 'منقطع':
            row['status'] = 'dropped'
        elif status == 'مغادر':
            row['status'] = 'left'

        if row['sex'] == 'أ':
            row['sex'] = 'f'
        else:
            row['sex'] = 'm'

    def after_save_instance(self, instance, using_transactions, dry_run):
        year = Year.objects.first()
        level = instance.grade
        status = 'passed'
        if not isinstance(level, int):
            if 'مكرر' in level:
                level = level.split('مكرر')[0].strip()
                status = 'repeated'
            if 'مكررة' in level:
                level = level.split('مكررة')[0].strip()
                status = 'repeated'
        Student.objects.create(
            child=instance,
            grade=Grade.objects.get(level=level, year=year),
            status=status
        )

