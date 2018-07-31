#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django
import requests
import openpyxl
import datetime,logging
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
from utils.upload_handler import UploadHandler

CURRENT_PATH = os.path.realpath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.realpath(os.path.join(CURRENT_PATH, os.pardir))
sys.path.insert(0, PROJECT_ROOT)

from base import load_django_settings

load_django_settings()
django.setup()

from django.conf import settings
from operation.models import Token
from operation.models import RoleInfo

APPID = settings.APPID
SECRET = settings.APP_SECRET

class ArmyImgImport():

    # def get(self, *args, **kwargs):
    #     pwd = self.get_argument("pwd", "")
    #     if not pwd or pwd != 'klm123':
    #         self.write(u'启动失败')
    #     else:
    #         filepath = u'C:/Users/klm/Desktop/八一/八一素材(2)/军旅素材'.encode('gbk')
    #         self.img_upload(filepath)


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

if __name__ == '__main__':
    army_db = ArmyImgImport()
    filepath = u'C:/Users/klm/Desktop/八一/八一素材(2)/军旅素材'.encode('gbk')
    army_db.img_upload(filepath)