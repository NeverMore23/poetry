# -*- coding: utf-8 -*-
# import logging
import sys
# print __file__
# print sys.path


# import logging
# logging.debug('debug message')
# logging.info('info message')
# logging.warning('warning message')
# logging.error('error message')
# logging.critical('critical message')

# logging.basicConfig(filename='/opt/poetry/log/log.txt',level=logging.DEBUG)
# logging.info('abc')
#
# try:
#     print abc
# except Exception:
#     logging.info('abc')

print 'hello'
print sys.stdout.write(('hello+\n'))

stdout_backup  = sys.stdout
log_file = open('massage.log','wb')
sys.stdout = log_file
print 'info here will be writing into massage.log'
log_file.close()
sys.stdout = stdout_backup

dict1 = {
    'a':12,
    'b':31,
    'c':9,
    'd':17
}

max_num = 0
name = None
for key,value in dict1.items():
    if value > max_num:
        max_num = value
        name = key
print name,max_num