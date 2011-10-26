#coding : utf8

import os
import sys
import string
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
from django.template.defaultfilters import slugify

### some helper functions


def get_exif(filename):
    ret = {}
    i = Image.open(filename)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def parse_filename(filename):
    ret = {}
    if (len(filename.split('_'))>=5):
        filename = str(filename)
        ret['name_full'] = filename
        ret['name'] = filename.split('.')[0]
        ret['slug'] = slugify(ret['name'][0:50])
        filename = filename.split('_')
        ret['date'] = datetime.strptime(filename[0],"%Y%m%d")
        #ret['photographer'] = str.capitalize(filename[-3]) +  ' ' + str.capitalize(filename[-2])
        ret['photographer'] = 'KSET'
    return ret

