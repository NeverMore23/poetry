# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
print 'ad'

a = 'abc'
c = b'abc'
b = a.encode()
print type(a)
print type(b)
print type(c)

s = "神话情话"
print s.decode('gbk')
print s.encode('gbk')
print s.decode()

url = "https://open.weixin.qq.com/connect/oauth2/authorize" \
              "?appid={}&redirect_uri=http%3A%2F%2Fe.klm123.com%2Fparty%2Fgrant%2Fuser={}" \
              "&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
APPID = '112334'
url = url.format(APPID, '')
print url