# -*- coding: utf-8 -*-
# tmp/test_script.py
# Usage : This script renames all images in 'media/images/children' from full_name.ext to subscription_id.ext

import os
from datetime import datetime

import django

os.environ["DJANGO_SETTINGS_MODULE"] = "kafili.settings"
django.setup()


from orphanage.models import *

start = datetime.now()
# ----------------------------------------------------------------
#  START SCRIPT
# ----------------------------------------------------------------


children = Child.objects.all()

basedir = settings.BASE_DIR
path = basedir + f'{MEDIA_URL}images/children'
if not os.path.exists(path):
    os.mkdir(path)
images_non_importees = []
multiples = []
count_images_importees = 0

for img in os.listdir(path):
    try:
        value = img.split('.')[0]

        child = children.get(full_name=value)

        new_name = f'{child.id}.{img.split(".")[1]}'
        os.rename(f'{path}/{img}', f'{path}/{new_name}')
        print(f'renamed_file: /{img} > /{new_name}')

    except ObjectDoesNotExist:
        images_non_importees.append(img)
    except MultipleObjectsReturned:
        multiples.append(img)

if images_non_importees:
    print('\n==================== NOT FOUND ====================')
    for img in images_non_importees:
        print('\t', img)
    print('===================================================')

if multiples:
    print('\n==================== MULTIPLES ====================')
    for img in multiples:
        print('\t', img)
    print('===================================================')


# ----------------------------------------------------------------
#  END SCRIPT
# ----------------------------------------------------------------
finish = datetime.now()
print(f'\n\nprocess finished in {(finish - start).total_seconds() * 10000} microseconds')
