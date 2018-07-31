#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import oss2
from django.conf import settings

logger = logging.getLogger("django")


class Alioss(object):
    AKID = "LTAIsUzOUaHLN282"
    AK_SEC = "eUQmpjncagnoUsEgGHgJx4yw6GqlAG"
    ENDPOINT = 'vpc100-oss-cn-beijing.aliyuncs.com'
    BUCKET = "klm-event"
    bucket = None

    @classmethod
    def set_up(cls):
        if cls.bucket is None:
            auth = oss2.Auth(cls.AKID, cls.AK_SEC)
            cls.bucket = oss2.Bucket(auth, cls.ENDPOINT, cls.BUCKET, connect_timeout=1)

    @classmethod
    def put_file(cls, name, path):
        cls.set_up()
        retry = 3
        while retry > 0:
            try:
                result = cls.bucket.put_object_from_file(name, path)
                return result
            except oss2.exceptions.RequestError as err:
                logging.error(err)
                retry -= 1

        raise ValueError(u"上传文件到阿里云失败")

    @classmethod
    def put_image(cls, name, data):
        cls.set_up()
        retry = 3
        while retry > 0:
            try:
                result = cls.bucket.put_object(name, data)
                return result
            except oss2.exceptions.RequestError as err:
                logging.error(err)
                retry -= 1

        raise ValueError(u"上传文件到阿里云失败")

    @classmethod
    def check_file(cls, file_name):
        cls.set_up()
        try:
            return cls.bucket.object_exists(file_name)
        except Exception as e:
            logging.error(e)
            return False


if __name__ == "__main__":
    Alioss.put_file("", "")

