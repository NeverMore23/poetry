import logging
from alioss import Alioss
import settings
import hashlib


class UploadHandler(object):
    @staticmethod
    def upload_file(file_data, file_name=None, file_type="jpg"):
        if not file_name:
            file_name = hashlib.md5(file_data).hexdigest() + "." + file_type
        remote_name = "{}{}".format('online/', file_name)
        Alioss.put_image(remote_name, file_data)

        # url = "http://" + settings.BUCKET + ".oss-cn-beijing.aliyuncs.com/" + remote_name
        url = "https://imageevent.klm123.com/" + remote_name
        logging.info(url)
        return url