# -*- coding: utf-8 -*-

from datetime import datetime
import re
import os

from django.template.defaultfilters import slugify

import filebrowser.settings as fb_settings
from PIL import Image
from PIL.ExifTags import TAGS


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
    if (len(filename.split('_')) >= 5):
        filename = str(filename)
        ret['name_full'] = filename
        ret['name'] = filename.split('.')[0]
        ret['slug'] = slugify(ret['name'][0:50])
        filename = filename.split('_')
        ret['date'] = datetime.strptime(filename[0], "%Y%m%d")
        ret['photographer'] = 'KSET'
    return ret


def exclude_fb_versions(album_dir):
    filter_re = [re.compile(exp) for exp in fb_settings.EXCLUDE]
    for exp in fb_settings.EXCLUDE:
        filter_re.append(re.compile(exp))
    for k, v in fb_settings.VERSIONS.iteritems():
        exp = (r'_%s(%s)') % (k, '|'.join(fb_settings.EXTENSION_LIST))
        filter_re.append(re.compile(exp))

    images = os.listdir(album_dir)
    for image in images:
        # EXCLUDE FILES MATCHING VERSIONS_PREFIX OR ANY OF THE EXCLUDE PATTERNS
        if not any(prefix.search(image) for prefix in filter_re):
            yield image
