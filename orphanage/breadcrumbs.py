from orphanage.utils import Page


home = Page(title='Home', label='الصفحة الرئيسية')
profile = Page(title='Profile', label='الملف الشخصي', parent=home)

year = Page(title='Year', label='السنة الدراسية', parent=home)
year_insert = Page(title='Year insert', label='إضافة سنة دراسية', parent=year)

children = Page(title='Children', label='لائحة الأطفال', parent=home)
child_insert = Page(title='Child insert', label='إضافة طفل', parent=children)
child_details = Page(title='Child details', label='البيانات الشخصية', parent=children)
child_update = Page(title='Child update', label='تحديث البيانات', parent=child_details)

grades = Page(title='Grades', label='لائحة المستويات الدراسية', parent=home)
grade_insert = Page(title='Grade insert', label='إضافة مستوى دراسي', parent=grades)
grade_details = Page(title='Grade details', label='بيانات المستوى الدراسي', parent=grades)
grade_update = Page(title='Grade update', label='تحديث المستوى الدراسي', parent=grade_details)


breadcrumbs = [
    home,
    profile,
    year, year_insert,
    children, child_insert, child_details, child_update,
    grades, grade_insert, grade_details, grade_update,
]


def get_page(page_title):

    for page in breadcrumbs:
        if page.title == page_title:
            return page
