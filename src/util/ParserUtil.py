import urllib.error as urle
from math import fabs

import cv2

import src.util.ImageUtil as iu


def getRealValue(value, realImageSize, default=0.0):
    return float(default) if value == '' else float(value) * realImageSize


def prepareImage(image, width=None, height=None):
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image

    if width is None:
        size = (height - h) / 2
        return cv2.copyMakeBorder(image, int(size), int(size), 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    else:
        size = (width - w) / 2
        return cv2.copyMakeBorder(image, 0, 0, int(size), int(size), cv2.BORDER_CONSTANT, value=[255, 255, 255])


def smartRectSelector(image, x1, x2, y1, y2, wRatio, hRatio):
    h, w = fabs(y2 - y1), fabs(x2 - x1)
    cw, ch = (h * wRatio / hRatio), (w * wRatio / hRatio)

    if (ch - h) > 0:
        # ch is new height
        return prepareImage(image[int(y1): int(y2), int(x1): int(x2)], height=int(ch))
    elif (cw - w) > 0:
        # cw is new wight
        return prepareImage(image[int(y1): int(y2), int(x1): int(x2)], width=int(cw))

    else:
        return image


def parse(dataset, location, wRatio, hRatio):
    print('file is {} and headers are {}'.format(location, next(dataset)))
    next(dataset)

    for idx, row in enumerate(dataset):
        url, name, x1, x2, y1, y2 = row
        try:
            image = iu.loadImage(url)
            image = smartRectSelector(image,
                                      getRealValue(x1, len(image[0])),
                                      getRealValue(x2, len(image[0]), len(image[0])),
                                      getRealValue(y1, len(image)),
                                      getRealValue(y2, len(image), len(image)),
                                      wRatio,
                                      hRatio)
            cv2.imwrite(location + '/{}.jpg'.format(idx), cv2.resize(image, (400, 400)))
        except urle.HTTPError:
            print('error: ', idx, ' row: ', row)
