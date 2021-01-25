
from orphanage import settings as orphanage_settings

def calculate_decision(mark):
    choices = orphanage_settings.STUDENT_DECISION_CHOICES
    if mark:
        if mark < 5:
            return 'F'  # راسب
        elif mark < 6:
            return 'C'  # مقبول
        elif mark < 7:
            return 'B'  # مستحسن
        elif mark < 8:
            return 'A'  # حسن
        else:
            return 'A+'  # حسن جدا
    return ''
