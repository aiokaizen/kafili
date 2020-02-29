# -*- coding: utf-8 -*-
# tmp/test_script.py
# Usage : You can do all your testings here. Overriding the file is not a problem

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

# code goes under
print(Child.import_photos())

# ----------------------------------------------------------------
#  END SCRIPT
# ----------------------------------------------------------------
finish = datetime.now()
print(f'\n\nprocess finished in {(finish - start).total_seconds() * 10000} microseconds')
