# -*- coding: utf-8 -*-
import os
import hashlib
import logging
import base64
import requests
import urllib, urllib2
import datetime

from django.conf import settings
from handlertypes import PageHandler, APIHandler, BaseHandler
from operation.models import User, Play, Counter, RoleInfo, UserImgInfo

from web.utils import errors
from utils.wechat import Wechat
from utils.alioss import Alioss
from utils.music import merge_music
from utils import generate_uid
from utils.upload_handler import UploadHandler



APPID = settings.APPID
SECRET = settings.APP_SECRET

# 这是图片存放路径
PICTURE_SAVE_PATH = "/opt/poetry/data/army/picture"


class ArmyDayHandler(PageHandler):

    def get(self, *args, **kwargs):
        url = self.request.full_url()
        token = Wechat.get_token(url)

        return self.render("armyday.html", token=token)


class ArmyDayUploadHandler(APIHandler):

    def post(self, *args, **kwargs):
        from web.utils.similarity import process

        source_img_data = self.request.files.get('headimg')
        if not source_img_data:
            raise errors.ArgumentError

        local_img_path = self.save_img(source_img_data[0]['body'])
        source_img_url = UploadHandler.upload_file(source_img_data[0]['body'])
        if not source_img_url:
            raise errors.PageError(u"图片上传失败")

        res = process(local_img_path)
        # res = {
        #     "name": u'许三多',
        #     "score": 0.70
        # }
        if not res:
            raise errors.PageError(u"图片识别失败")
        try:
            os.remove(local_img_path)
        except Exception as e:
            logging.error(e)

        try:
            role_info = RoleInfo.objects.get(name=res["name"])
        except Exception as e:
            raise e

        try:
            img_info = UserImgInfo()
            img_info.source_img_url = source_img_url
            img_info.role_img_url = role_info.role_img_url
            img_info.role = res["name"]
            img_info.similarity = "%.2f" % (res["score"]*100)
            img_info.save()
        except Exception as e:
            logging.exception(e)

        result = {
            "code": 0,
            'source_img_url': source_img_url,
            'role_img_url': role_info.role_img_url,
            'share_ico_url': role_info.share_ico_url,
            'role_name': role_info.name,
            'role_abstract': role_info.abstract,
            'similarity': "%.2f" % (res["score"]*100)
        }

        self.write(result)

    def save_img(self, img_data):
        name = hashlib.md5(img_data).hexdigest()

        local_img_path = PICTURE_SAVE_PATH + name + '.jpg'
        with open(local_img_path, 'wb')as f:
            f.write(img_data)
        print local_img_path
        return local_img_path

        # def img_download(self, img_url):
        #     local_img_path = PICTURE_SAVE_PATH + 'temp.jpg'
        #
        #     try:
        #         load_data = urllib.urlretrieve(img_url, local_img_path)
        #     except IOError as e:
        #         logging.exception(e)
        #         raise errors.PageError(u"源图下载失败")
        #
        #     with open(load_data[0], 'rb') as f:
        #         img_content = f.read()
        #     return img_content


class ArmyDayDBHandler(APIHandler):

    def get(self, *args, **kwargs):
        pwd = self.get_argument("pwd", "")
        if not pwd or pwd != 'klm123':
            self.write(u'启动失败')
        else:
            filepath = u'C:/Users/klm/Desktop/八一/八一素材(2)/军旅素材'.encode('gbk')
            self.img_upload(filepath)


    def iteratorFile(self, filepath):
        for root, dirs, files in os.walk(filepath):
            for f in files:
                yield os.path.join(root, f)


    def img_upload(self, filepath):
        file_list = self.iteratorFile(filepath)
        fail_count = success_count = 0

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
                    img_name = img_name[:len(img_name) - 1]
                    print 2, img_name.split('\\')[-1].decode('gbk').encode('utf-8').strip()
                    print source_img_url.strip()
                    userimginfo = RoleInfo.objects.get(
                        name=img_name.split('\\')[-1].decode('gbk').encode('utf-8').strip())
                    userimginfo.create_time = datetime.datetime.now()
                    userimginfo.modify_time = datetime.datetime.now()
                    userimginfo.share_ico_url = source_img_url
                    userimginfo.save()
                else:
                    print 1, img_name.split('\\')[-1].decode('gbk').encode('utf-8').strip()
                    print source_img_url
                    userimginfo = RoleInfo.objects.get(
                        name=img_name.split('\\')[-1].decode('gbk').encode('utf-8').strip())
                    userimginfo.create_time = datetime.datetime.now()
                    userimginfo.modify_time = datetime.datetime.now()
                    userimginfo.role_img_url = source_img_url
                    userimginfo.save()
                success_count += 1
            except Exception:
                fail_count += 1
                # logging.error(u'失败%s'%img_name)
                continue

        print u'成功%s，失败 %s 条' % (success_count, fail_count)
