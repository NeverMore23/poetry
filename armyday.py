# -*- coding: utf-8 -*-
import os
import hashlib
import logging
import base64
import requests
import urllib, urllib2

from django.conf import settings
from handlertypes import PageHandler, APIHandler, BaseHandler
from operation.models import User, Play, Counter, RoleInfo, UserImgInfo

from web.utils import errors
from utils.wechat import Wechat
from utils.alioss import Alioss
from utils.music import merge_music
from utils import generate_uid
from utils.upload_handler import UploadHandler

from web.utils.similarity_calc import similarity_calc

APPID = settings.APPID
SECRET = settings.APP_SECRET

# 这是图片存放路径
PICTURE_SAVE_PATH = "d:\\opt\\poetry\\data\\"


class ArmyDayHandler(APIHandler):
    def get(self, *args, **kwargs):
        source_img_url = self.get_argument("source_url", "")
        if not source_img_url:
            raise errors.ArgumentError

        print '*' * 100
        print source_img_url
        source_img_data = self.img_download(source_img_url)

        res = similarity_calc(source_img_data)

        compose_img_data = res['compose_img_content']
        if not compose_img_data:
            raise errors.PageError(u"图片识别失败")

        try:
            compose_img_url = UploadHandler.upload_file(compose_img_data)
        except Exception as e:
            raise errors.PageError(u"图片上传失败")

        try:
            os.remove(PICTURE_SAVE_PATH + 'temp.jpg')
        except Exception as e:
            logging.exception(e)

        # imginfo = UserImgInfo()
        # imginfo.source_img_url = source_img_url
        # imginfo.compose_img_url = compose_img_url
        # imginfo.save()
        #
        # try:
        #     role_info = RoleInfo.objects.get(id=res['role_id'])
        # except Exception as e:
        #     logging.exception(e)

        data = {
            'source_img_url': source_img_url,
            'compose_img_url': compose_img_url,
            'share_ico_url': 'role_info.share_ico_url',
            'role_name': 'role_info.name',
            'role_abstract': 'role_info.abstract',

        }

        # self.write(data)
        self.render("back.html", data=data)

    def img_download(self, img_url):
        local_img_path = PICTURE_SAVE_PATH + 'temp.jpg'

        try:
            load_data = urllib.urlretrieve(img_url, local_img_path)
        except IOError as e:
            logging.exception(e)
            raise errors.PageError(u"源图下载失败")

        with open(load_data[0], 'rb') as f:
            img_content = f.read()
        return img_content


class UploadImageHandler(APIHandler):
    def post(self):
        data = self.get_argument("data", "")
        if not data:
            raise errors.ArgumentError

        data = base64.b64decode(data)
        url = UploadHandler.upload_file(data, 'jpg')
        result = {
            "code": 0,
            "data": {
                "url": url
            }
        }
        # self.write(result)
        self.render("play_detail.html", result=result)
