# -*- coding: utf-8 -*-
import os
import hashlib
import logging
import base64
import requests
import urllib, urllib2
from django.conf import settings
from alioss import Alioss
from upload import UploadHandler


def iteratorFile(filepath):
    for root, dirs, files in os.walk(filepath):
        for f in files:
            yield os.path.join(root, f)


def img_upload(filepath):
    file_list = iteratorFile(filepath)
    for file in file_list:
        img_name = os.path.splitext(file)[0]
        with open(file, 'rb') as f:
            content = f.read()
        source_img_url = None
        try:
            source_img_url = UploadHandler.upload_file(content)
        except Exception as e:
            logging.exception(e)

        try:
            if img_name.endswith('z'):
                pass
            elif img_name.endswith('2'):
                pass
                # img_name = img_name[:len(img_name) - 1]
                # print 2, img_name.split('\\')[-1].decode('gbk').encode('utf-8')
                # print source_img_url
                # userimginfo = UserImgInfo.objects.get(name=img_name.split('\\')[-1])
                # userimginfo.share_ico_url = source_img_url
                # userimginfo.save()
            else:
                print 1, img_name.split('\\')[-1].decode('gbk').encode('utf-8').strip()
                print source_img_url
                # userimginfo = UserImgInfo.objects.get(name=img_name.split('\\')[-1])
                # userimginfo.role_img_url = source_img_url
                # userimginfo.save()

        except Exception:
            pass
            # raise errors.DBError


# remote_name = "{}{}".format(settings.UPLOAD_PREFIX, file_name)
# url = "https://imageevent.klm123.com/" + remote_name
filepath = u'C:/Users/klm\Desktop/八一/八一素材(1)/军旅角色素材'.encode('gbk')
img_upload(filepath)
