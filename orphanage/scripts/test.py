# -*- coding: utf-8 -*-
# tmp/test_script.py
# Usage : You can do all your testings here. Overriding the file is not a problem

import os
from datetime import datetime

import django
from django.conf import settings
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from kafili.settings import MEDIA_URL

os.environ["DJANGO_SETTINGS_MODULE"] = "kafili.settings"
django.setup()

from orphanage.models import *

start = datetime.now()
# ----------------------------------------------------------------
#  START SCRIPT
# ----------------------------------------------------------------

# code goes under
children = Child.objects.all()

basedir = settings.BASE_DIR
path = basedir + f'{MEDIA_URL}images/children'
if not os.path.exists(path):
    os.mkdir(path)
images_non_importees = []
count_images_importees = 0

for img in os.listdir(path):
    try:
        value = img.split('.')[0]

        if not value.isdigit():
            continue

        child = children.get(id=value)
        if not child.picture or 1:

            # child.picture = '/images/children/' + img
            # count_images_importees += 1
            # child.save()

            # response = urllib2.urlopen("http://path.to.file/img.jpg")
            # with open('tmp_img', 'wb') as f:
            #     f.write(response.read())

            with open(f'{path}/{img}', 'rb') as f:
                image_file = File(f)
                print('file:', image_file)
                child.picture.save(img, image_file, True)
                child.save()

            # Rename the img file from full name to id
            # os.rename(f'{path}/{img}', f'{path}/{child.id}.{img.split(".")[1]}')
            # print(f'renamed_file: /{img} > /{child.id}.{img.split(".")[1]}')

    except ObjectDoesNotExist:
        images_non_importees.append(img)
    except MultipleObjectsReturned:
        print(f'multiple: {value}')

if images_non_importees:
    non_importees = ''
    for img in images_non_importees:
        non_importees += img + '; '
    message = ('warning', f'({len(images_non_importees)}/{len(os.listdir(path))}) Images non importées: {non_importees}')
    print(message)

message = ('success', f"{count_images_importees} images ont été importer.")
print(message)

# for child in children:
#     if child.picture:
#         print(f'child: {child}; pic: {child.picture.url}')
#     else:
#         print('no pic')


# ----------------------------------------------------------------
#  END SCRIPT
# ----------------------------------------------------------------
finish = datetime.now()
print(f'\n\nprocess finished in {(finish - start).total_seconds() * 10000} microseconds')
