from upload import UploadHandler

PICTURE_SAVE_PATH = 'd:\\sina.jpg'

with open(PICTURE_SAVE_PATH,'rb') as f:
    content = f.read()

result_url = UploadHandler.upload_file(content)
print result_url


# upload_file 函数中的有关settings的配置remote_name---在my_settings中
# alioss中ENDPOINT的配置 在 settings中
# 修改了 alioss中和Upload中两个settings配置