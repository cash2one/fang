# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from os import environ as _env
from urlparse import urlparse
from celery.schedules import crontab

from .error_codes import error_codes


# 线上环境用Calypso 配置，所以做一个environ 的代理
class CalypsoEnv(object):
    def get(self, key, default=None):
        value = _env.get(key)

        # 相当于重定向
        alias = _env.get(value)
        if alias is not None:
            return alias

        if not value and default:
            return default
        return value

environ = CalypsoEnv()


class EnvConfigType(type):

    def __getattribute__(cls, key):
        value = object.__getattribute__(cls, key)
        env = environ.get(key)

        if env is not None:
            value = type(value)(env)
        return value


class Config(object):

    __metaclass__ = EnvConfigType

    DEBUG = True
    TESTING = False

    SECRET_KEY = '53a01e6bd34feef997eed2425ee9d3e0'
    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (
        environ.get('PG_USER', 'sub'),
        environ.get('PG_PASSWORD', 'ssss'),
        environ.get('POSTGRES_PORT_5432_TCP_ADDR', 'localhost'),
        environ.get('POSTGRES_PORT_5432_TCP_PORT', '5432'),
        environ.get('PG_DATABASE', 'sub'))
    SQLALCHEMY_SLAVE_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (
        environ.get('PG_USER', 'sub'),
        environ.get('PG_PASSWORD', 'ssss'),
        environ.get('SLAVE_POSTGRES_PORT_5432_TCP_ADDR', 'localhost'),
        environ.get('SLAVE_POSTGRES_PORT_5432_TCP_PORT', '5432'),
        environ.get('PG_DATABASE', 'sub'))
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_BINDS = {
        'master': SQLALCHEMY_DATABASE_URI,
        'slave': SQLALCHEMY_SLAVE_DATABASE_URI
    }

    COEFFICIENT = float(environ.get('COEFFICIENT', 0.72))

    REDIS_MASTER_HOST = environ.get('REDIS_PORT_6379_TCP_ADDR', 'localhost')
    REDIS_MASTER_PORT = environ.get('REDIS_PORT_6379_TCP_PORT', '6379')
    REDIS_DATABASE = environ.get('REDIS_DATABASE', '4')
    REDIS_MASTER_URL = 'redis://%s:%s/%s' % (REDIS_MASTER_HOST,
                                             REDIS_MASTER_PORT,
                                             REDIS_DATABASE)
    REDIS_MASTER_SERVER = {
        'host': REDIS_MASTER_HOST,
        'port': REDIS_MASTER_PORT,
        'db': REDIS_DATABASE,
    }

    REDIS_SLAVE_HOST = environ.get('REDIS_SLAVE_PORT_6379_TCP_ADDR',
                                   'localhost')
    REDIS_SLAVE_PORT = environ.get('REDIS_SLAVE_PORT_6379_TCP_PORT', '6379')
    REDIS_SLAVE_URL = 'redis://%s:%s/%s' % (REDIS_SLAVE_HOST, REDIS_SLAVE_PORT,
                                            REDIS_DATABASE)
    REDIS_SLAVES_SERVER = [
        {
            'host': REDIS_SLAVE_HOST,
            'port': REDIS_SLAVE_PORT
        },
    ]

    MEMCACHED_URLS = environ.get('MEMCACHED_URLS', 'localhost:11211')

    # celery settings
    CELERY_BROKER_URL = 'amqp://{username}:{password}@{host}:{port}/sub'.format(
        username=environ.get('CELERY_RABBITMQ_PORT_5672_USERNAME', 'sub'),
        password=environ.get('CELERY_RABBITMQ_PORT_5672_PASSWORD', 'sub'),
        host=environ.get('CELERY_RABBITMQ_PORT_5672_TCP_ADDR', 'localhost'),
        port=environ.get('CELERY_RABBITMQ_PORT_5672_TCP_PORT', '5672'))
    CELERY_RESULT_BACKEND = 'rpc://{username}:{password}@{host}:{port}/sub'.format(
        username=environ.get('CELERY_RABBITMQ_PORT_5672_USERNAME', 'sub'),
        password=environ.get('CELERY_RABBITMQ_PORT_5672_PASSWORD', 'sub'),
        host=environ.get('CELERY_RABBITMQ_PORT_5672_TCP_ADDR', 'localhost'),
        port=environ.get('CELERY_RABBITMQ_PORT_5672_TCP_PORT', '5672'))
    CELERY_ALWAYS_EAGER = False
    CELERY_TIMEZONE = 'Asia/Shanghai'

    STATIC_FOLDER = 'static'

    FENDA_DOMAIN = environ.get('FENDA_DOMAIN', 'http://zhitest.zaih.com')
    CENSOR_DOMAIN = environ.get('CENSOR_DOMAIN', 'http://test-fd-censor.zaih.com')
    APP_TRANSPORT = environ.get('APP_TRANSPORT', 'http')
    APP_DOMAIN = environ.get('APP_DOMAIN', 'http://sub-test.zaih.com')
    DOMAIN = '%s://%s' % (APP_TRANSPORT, urlparse(APP_DOMAIN).netloc)

    FENDA_SERVER_HOST = environ.get('FENDA_PORT_8888_HTTP_PROTO',
                                    'http://localhost:8888')
    FENDA_OAUTH_API = '{host}/backend/oauth/tokeninfo'.format(host=FENDA_SERVER_HOST)
    FENDA_BACKEND_API = '{host}/backend'.format(host=FENDA_SERVER_HOST)
    OAUTH_SERVER_HOST = environ.get('OAUTH_PORT_8897_HTTP_PROTO', 'http://localhost:8897')
    FENDA_AUTH_BACKEND_API = '{host}/backend'.format(host=OAUTH_SERVER_HOST)
    FENDA_ACCOUNT_BACKEND_API = '{host}/backend'.format(host=FENDA_SERVER_HOST)
    # censor server
    CENSOR_SERVER_HOST = environ.get('CENSOR_PORT_8989_HTTP_PROTO', 'http://localhost:8989')
    CENSOR_BACKEND_API = '{host}/backend'.format(host=CENSOR_SERVER_HOST)
    # board server
    BOARD_SERVER_HOST = environ.get('BOARD_PORT_8889_HTTP_PROTO', 'http://0.0.0.0:8889')
    BOARD_BACKEND_API = '{host}/backend'.format(host=BOARD_SERVER_HOST)
    # feed server
    FEED_SERVER_HOST = environ.get('FEED_PORT_8891_HTTP_PROTO', 'http://localhost:8891')
    FEED_BACKEND_API = '{host}/backend'.format(host=FEED_SERVER_HOST)
    # bank server
    BANK_SERVER_HOST = environ.get('BANK_PORT_8898_HTTP_PROTO', 'http://localhost:8898')
    BANK_BACKEND_API = '{host}/backend'.format(host=BANK_SERVER_HOST)

    BACKEND_APIS = {
        'auth': FENDA_AUTH_BACKEND_API,
        'account': FENDA_ACCOUNT_BACKEND_API,
        'censor': CENSOR_BACKEND_API,
        'board': BOARD_BACKEND_API,
        'feed': FEED_BACKEND_API,
        'fenda': FENDA_BACKEND_API,
        'bank': BANK_BACKEND_API,
    }

    REVIEW_SERVER_HOST = environ.get('REVIEW_SERVER_HOST', b'54.223.60.47')
    REVIEW_SERVER_PORT = environ.get('REVIEW_SERVER_PORT', b'8008')
    REVIEW_SERVER_URL = "http://%s:%s/api/v1/blacklist" % (REVIEW_SERVER_HOST,
                                                           REVIEW_SERVER_PORT)
    REVIEW_SERVER_USERNAME = environ.get('REVIEW_SERVER_USERNAME', b'')
    REVIEW_SERVER_PASSWORD = environ.get('REVIEW_SERVER_PASSWORD', b'')

    # SENTRY DNS
    SENTRY_DSN = ('http://1719faec88124a8dbaf19f795c7347a7:'
                  '46988a33167d47b380e85972215c8ad4@sentry.iguokr.com:5000/12')

    # 微信小程序 账号信息
    WXAPP_APPID = environ.get('WXAPP_APPID', 'wxappid')
    WXAPP_SECRET = environ.get('WXAPP_SECRET', 'wxappsecret')

    # 微信 公众账号信息
    WEIXINMP_APPID = environ.get('WEIXINMP_APPID', 'wxba29bd8df2c92c95')
    WEIXINMP_APP_SECRET = environ.get('WEIXINMP_APP_SECRET',
                                      '5aaac0b823e6ec599f932959ab179481')
    WEIXINMP_TOKEN = environ.get('WEIXINMP_TOKEN',
                                 'OHBlcWfhMUHczZDMxNWJjMDRkZTJiOGE')
    WEIXINMP_ENCODINGAESKEY = environ.get(
        'WEIXINMP_ENCODINGAESKEY',
        '9On5TSh45id6e9RNakfPkbaElU6nZlA2ZNFe6K9fuof')

    # 微信appid 移动应用
    WEIXINAPP_APPID = environ.get('WEIXINAPP_APPID', 'wx8d596a03f69aaa8f')
    WEIXINAPP_APPSECRET = environ.get(
        'WEIXINAPP_APPSECRET', 'd68bc46520369c70f407fea408ae27ae')

    QINIU_ACCESS_TOKEN = 'x7cu88uRBgDKIWHzGHvK-OgKznQpY4ZfhbObIrt2'
    QINIU_SECRET_TOKEN = 'btfJJE_RuWdlX9C9Ww3Y3a2ayVBwDF5lKKsRLs7c'
    QINIU_UPLOAD_URL = 'http://up.qiniu.com/'
    QINIU_DOMAIN = environ.get('QINIU_DOMAIN', 'medias.zaih.com')
    QINIU_DOMAINS = [QINIU_DOMAIN, 'oddfrn1vt.qnssl.com',
                     'dn-zaih.qbox.me', 'media.zaih.com', 'hangjia.qiniudn.com']
    QINIU_HOST = "https://%s" % QINIU_DOMAIN
    QINIU_NOTIFY_URL = '%s/py/qiniu/pfop/notify' % DOMAIN
    QINIU_PUBLIC_BUCKET = 'hangjia'
    # 私有空间域名
    QINIU_PRIVITE_DOMAIN = environ.get('QINIU_PRIVITE_DOMAIN', 'audio.zaih.com')
    QINIU_PRIVITE_HOST = "http://%s" % QINIU_PRIVITE_DOMAIN
    QINIU_PRIVITE_BUCKET = 'fenda-media'
    QINIU_PIPELINE = environ.get('QINIU_PIPELINE', 'zaih_media')
    QINIU_FILTER_NOTIFY_URL = '%s/py/qiniu/pfop/filter_notify' % DOMAIN
    QINIU_RECOGNITION_NOTIFY_URL = '%s/py/qiniu/pfop/recognition_notify' % CENSOR_DOMAIN
    QINIU_AUDIOS_TIME_KEY = environ.get('QINIU_AUDIOS_TIME_KEY',
                                        '4db9bf9acfaa16a859a85b9b3f89e88a56997fb9')
                                        # '769a2b8966b87ebbcea9a5b95bbba4a8a88a57b9')
    QINIU_AUDIOS_HOST = environ.get('QINIU_AUDIOS_HOST', 'https://audios.zaih.com')
    QINIU_AUDIOS_CONFIG = {
        'access_key': QINIU_ACCESS_TOKEN,
        'secret_key': QINIU_SECRET_TOKEN,
        'time_key': QINIU_AUDIOS_TIME_KEY,
        'host': QINIU_AUDIOS_HOST
    }

    # jpush config
    JPUSH_APP_KEY = environ.get('JPUSH_APP_KEY', '')
    JPUSH_MASTER_SECRET = environ.get('JPUSH_MASTER_SECRET', '')

    ERROR_CODES = error_codes

    # 错误通知接受者openid
    ADMIN_OPENID = environ.get('ADMIN_OPENID', 'o7l9Gs_IyQhSH1esMb50zxGnhdwc')

    APP_CLIENT_ID = 'sub'
    APP_CLIENT_SECRET = 'm78QY7TkHwBDScJv8nEaJiOgcmi9'

    ALLOW_CLIENTS = ['weixin', 'panel', 'ios', 'android']

    # 创蓝短信
    CLSMS_API_URL = environ.get(
        'CLSMA_API_URL', 'http://222.73.117.156:80/msg/HttpBatchSendSM')
    CLSMS_ACCOUNT = environ.get('CLSMS_ACCOUNT', '')
    CLSMS_PASSWORD = environ.get('CLSMS_PASSWORD', '')
    CLSMS_ACCOUNT_MARKETING = environ.get('CLSMS_ACCOUNT_MARKETING', '')
    CLSMS_PASSWORD_MARKETING = environ.get('CLSMS_PASSWORD_MARKETING', '')

    CELERYBEAT_SCHEDULE = {
    }
