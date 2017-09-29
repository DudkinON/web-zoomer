import hashlib
import os
from random import random
from PIL import Image


def image_resize(data, output_size):
    """Resize image for thumbnails and preview
    data — image for resize
    output_size — turple, contains width and height of output image,
    for example (200, 500)

    :param data:
    :param output_size:
    :return file:
    """

    image = Image.open(data)
    m_width = float(output_size[0])
    m_height = float(output_size[1])
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
    w_k = image.size[0] / m_width
    h_k = image.size[1] / m_height
    if output_size < image.size:
        if w_k > h_k:
            new_size = (m_width, image.size[1] / w_k)
        else:
            new_size = (image.size[0] / h_k, m_height)
    else:
        new_size = image.size
    return image.resize(new_size, Image.ANTIALIAS)


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
    # instance = image_resize(instance, conf.IMAGE_UPLOAD_SIZE)
    return '{0}/{1}'.format(path_to_img, filename)


