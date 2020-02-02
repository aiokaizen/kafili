from orphanage.utils import Page


home = Page(title='Home', label='الصفحة الرئيسية')
profile = Page(title='Profile', label='الملف الشخصي', parent=home)
children = Page(title='Children', label='لائحة الأطفال', parent=home)
child_insert = Page(title='Child insert', label='إضافة طفل', parent=children)
child_details = Page(title='Child details', label='البيانات الشخصية', parent=children)
child_update = Page(title='Child update', label='تحديث البيانات', parent=child_details)


breadcrumbs = [
    home, profile, children, child_insert, child_details, child_update
]


def get_page(page_title):

    for page in breadcrumbs:
        if page.title == page_title:
            return page
