from __future__ import unicode_literals

import hashlib
import os
from random import random


def get_image_path(instance, filename):
    """Create path to image

    :param instance:
    :param filename:
    :return:
    """
    ext = filename.split('.')[-1]
    hash_ = hashlib.md5()
    hash_.update(repr(random()).encode('utf-8'))
    hash_name = hash_.hexdigest()
    path_to_img = os.path.join('article_images', hash_name[:2], hash_name[2:4],
                               hash_name[4:6])
    filename = '{0}.{1}'.format(hash_name[6:], ext)

    return '{0}/{1}'.format(path_to_img, filename)


