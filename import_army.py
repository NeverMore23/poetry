#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django
import requests
import openpyxl
import datetime
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook

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


def import_army_data(excel_path):

    wb = load_workbook(excel_path)
    ws = wb.active


    for row in ws.rows:
        roleinfo = RoleInfo()
        n = 0
        for col in row:
            if n in [0,1,2]:
                pass
            elif n == 3:
                print 'a',col.value
                roleinfo.name = col.value
            elif n == 4:
                print 'b',col.value
                roleinfo.abstract = col.value
            elif n == 5:
                print 'c',col.value
                roleinfo.role_tv = col.value
            elif n == 6:
                print 'd',col.value
                roleinfo.role_img_url = col.value
            elif n == 7:
                print 'e',col.value
                roleinfo.share_ico_url = col.value
            roleinfo.create_time = datetime.datetime.now()
            roleinfo.modify_time_time = datetime.datetime.now()
            roleinfo.save()
            n += 1

if __name__ == "__main__":
    excel_path = 'C:/Users/klm/Desktop/operation_roleinfo.xlsx'
    import_army_data(excel_path)
