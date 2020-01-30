from django.forms import ClearableFileInput, DateInput


class DateWidget(DateInput):
    template_name = 'orphanage/widgets/date.html'


class ImageWidget(ClearableFileInput):
    initial_text = 'الصورة الحالية'
    input_text = 'تغيير الصورة'
    clear_checkbox_label = 'مسح'
    template_name = 'orphanage/widgets/picture.html'
