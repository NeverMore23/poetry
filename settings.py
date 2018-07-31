# -*- coding: utf-8 -*-
"""
Django settings for app project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import sys
import os.path

reload(sys)
sys.setdefaultencoding('utf-8')

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))


def load_settings(settings, debug=False, **kwargs):
    settings.update(
        {
            "MENU_CONFIG": [
                {
                    "id": "menu_video",
                    "name": u"诗歌管理",
                    "children": [
                        {
                            "name": u"用户诗歌",
                            "path": "/operation/play/list",
                        },
                    ]
                },
                {
                    "id": "menu_user",
                    "name": u"用户管理",
                    "children": [
                        {
                            "name": u"用户列表",
                            "path": "/operation/user/list",
                        },
                    ]
                },
                {
                    "id": "menu_admin",
                    "name": u"系统管理",
                    "path": "/admin",
                },
            ],

            'ALLOWED_HOSTS': ['*'],
            'DATABASES': {
                # 'default': {
                #     'ENGINE': 'django.db.backends.mysql',
                #     'NAME': 'klm_activity',
                #     'USER': 'klm_activity',
                #     'PASSWORD': 'PZGBfEXZSCsoQ7c8',
                #     'HOST': 'rm-2ze0pk59z179yavjj.mysql.rds.aliyuncs.com',
                #     'PORT': '',  # Set to empty string for default.
                #     'OPTIONS': {
                #         'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                #         "charset": "utf8mb4",
                #     }
                # },
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': 'klm_activity',
                    'USER': 'klm_activity',
                    'PASSWORD': 'PZGBfEXZSCsoQ7c8',
                    'HOST': 'rm-2ze0pk59z179yavjj.mysql.rds.aliyuncs.com',
                    'PORT': '',  # Set to empty string for default.
                    'CONN_MAX_AGE': 86400 * 365,
                    'OPTIONS': {
                        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                        "charset": "utf8mb4",
                    }
                },
            },

            'LANGUAGES': [
                ('en', 'English'),
            ],

            'TRANSMETA_DEFAULT_LANGUAGE': 'zh-cn',
            'TIME_ZONE': 'Asia/Shanghai',
            # 'LANGUAGE_CODE': 'zh_cn',
            'SITE_ID': 1,
            'USE_I18N': False,
            'USE_L10N': False,
            'MEDIA_ROOT': '',
            'MEDIA_URL': '',
            'STATIC_ROOT': '',
            'STATIC_URL': '/static/',
            'ADMIN_MEDIA_PREFIX': '/static/admin/',
            'SECRET_KEY': 'ovvxva)f_gx7$ldaasbn+l2asdfaadfdsafasdf2##sdfsa',
            'AUTHENTICATION_BACKENDS': (
                "django.contrib.auth.backends.ModelBackend",
            ),

            "TEMPLATES": [
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'APP_DIRS': True,
                    'DIRS': [
                        os.path.join(PROJECT_ROOT, "templates"),
                        os.path.join(PROJECT_ROOT, "videocenter/templates"),
                    ],
                    'OPTIONS': {
                        'debug': False,
                        'context_processors': (
                            'django.template.context_processors.debug',
                            'django.template.context_processors.request',
                            'django.contrib.auth.context_processors.auth',
                            'django.contrib.messages.context_processors.messages',
                        ),
                    }
                },
            ],

            "LOGGING": {
                'version': 1,
                'disable_existing_loggers': False,
                'formatters': {
                    'verbose': {
                        'format': '%(levelname)s %(asctime)s %(module)s:%(lineno)d %(message)s'
                    },
                    'simple': {
                        'format': '%(levelname)s %(message)s'
                    },
                },
                'handlers': {
                    'file': {
                        'level': 'DEBUG',
                        'class': 'logging.FileHandler',
                        'filename': '/opt/poetry/log/django.log',
                        'formatter': 'verbose'
                    },
                    'operation': {
                        'level': 'DEBUG',
                        'class': 'logging.FileHandler',
                        'filename': '/opt/poetry/log/operation.log',
                        'formatter': 'verbose'
                    },
                    'console': {
                        'level': 'DEBUG',
                        'class': 'logging.StreamHandler',
                        'formatter': 'verbose'
                    },
                },
                'loggers': {
                    'django': {
                        'handlers': ['file', 'console'],
                        'level': 'INFO',
                        'propagate': True,
                    },
                    # 'django.db.backends': {
                    #     'handlers': ['console'],
                    #     'propagate': True,
                    #     'level': 'DEBUG',
                    # },
                    'operation': {
                        'handlers': ['operation', 'console'],
                        'level': 'INFO',
                        'propagate': True,
                    },
                },
            },
            'DEBUG': True,
            'TEST': False,
            'PROJECT_ROOT': PROJECT_ROOT,
            'DATETIME_FORMAT': 'Y-n-d H:i:s',

            'ROOT_URLCONF': 'urls',
            'STATICFILES_FINDERS': [
                'django.contrib.staticfiles.finders.FileSystemFinder',
                'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            ],
            'STATICFILES_DIRS': (
                os.path.join(PROJECT_ROOT, 'static'),
            ),

            'MIDDLEWARE': [
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'permission.middleware.PermMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
            ],

            'INSTALLED_APPS': [
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                # 'django.contrib.sites',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'django.contrib.admin',
                'django.contrib.admindocs',
                'el_pagination',
                'operation',
                'permission',
            ],
            "LOGIN_URL": "/signin",
            "LOGIN_REDIRECT_URL": "/",

            "ALWAYS_ALLOWED_PERMS": ("signout/$", "signin/$"),

            "APPID": "wx0411602eda8e17bd",
            "APP_SECRET": "bfbb109a87b5c7b996f891d7d848b1f0",
            "BUCKET": "klm-event",
            "ENDPOINT": "vpc100-oss-cn-beijing.aliyuncs.com",

            "ENV": "online",
            "UPLOAD_PREFIX": "online/",
            "MEDIA_PATH": "/opt/poetry/data/media",
            "IMAGE_PATH": "/opt/poetry/data/image",
        },
    )
