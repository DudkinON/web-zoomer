from __future__ import unicode_literals

import hashlib
import os
from random import random
from json import dumps
from web_zoomer_com.settings import ARTICLE_IMG_ROOT, USER_AVATAR_ROOT
from random import choice
from string import ascii_uppercase as uppercase, digits


def get_path(instance, filename, folder):
    """Create path

    :param instance:
    :param filename:
    :param folder:
    :return string:
    """
    ext = filename.split('.')[-1]
    hash_ = hashlib.md5()
    hash_.update(repr(random()).encode('utf-8'))
    hash_name = hash_.hexdigest()
    path_to_img = os.path.join(folder, hash_name[:2], hash_name[2:4],
                               hash_name[4:6])
    filename = '{0}.{1}'.format(hash_name[6:], ext)
    return '{0}/{1}'.format(path_to_img, filename)


def get_image_path(instance, filename):
    """Return path for article image

    :param instance:
    :param filename:
    :return string:
    """
    return get_path(instance, filename, ARTICLE_IMG_ROOT)


def get_user_image_path(instance, filename):
    """Return path for user avatar

    :param instance:
    :param filename:
    :return string:
    """
    return get_path(instance, filename, USER_AVATAR_ROOT)


def get_unique_str(amount):
    """
    Return a unique name string amount characters
    :return:
    """
    return ''.join(choice(uppercase + digits) for x in range(amount))


def get_json(data):
    """
    Get dictionary and return JSON string with UTF-8

    :param data: dict
    :return: string
    """
    return dumps(data, ensure_ascii=False)
