# -*- coding: utf-8 -*-
import time
import string
import random
import urllib

from urlparse import urlparse
from hashlib import md5

import requests
from requests.exceptions import ConnectTimeout, ReadTimeout

from flask import current_app as app
from qiniu import Auth, PersistentFop, op_save, BucketManager

from sub.settings import Config

from zaih_core.caching import cache_for
from zaih_core.coding import smart_str


def generate_nonce_str(length=32):
    return ''.join(random.SystemRandom().choice(
        string.ascii_letters + string.digits) for _ in range(length))


def get_qiniu_file_avinfo(url):
    try:
        req = requests.get(url)
    except (ConnectTimeout, ReadTimeout):
        return {}
    if req.status_code == 200:
        info = req.json()
        return info.get('format', {})
    return {}


def get_qiniu_file_duration(url):
    '''七牛私有空间音频资源avinfo中duration'''
    info = get_qiniu_file_avinfo(url)
    if not info:
        return None
    duration = info.get('duration', 0)
    try:
        duration = int(float(duration) + 0.5)
        return duration
    except ValueError:
        return None


def get_qiniu_file_size(url):
    '''七牛私有空间音频资源avinfo中duration'''
    info = get_qiniu_file_avinfo(url)
    if not info:
        return None
    size = info.get('size', 0)
    try:
        size = int(size) / 1000
        return size
    except ValueError:
        return None


def get_qiniu_file_md5(url):
    try:
        req = requests.get(url)
    except (ConnectTimeout, ReadTimeout):
        return ''
    if req.status_code == 200:
        info = req.json()
        return info.get('md5', '')
    return ''


class QiniuUriGen():

    __version__ = '1.0'

    def __init__(self, access_key=None, secret_key=None,
                 time_key=None, host=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.time_key = time_key
        self.host = host

    def url_encode(self, s):
        return urllib.quote(smart_str(s), safe="/")

    def t16(self, t):
        return hex(t)[2:].lower()

    def to_deadline(self, expires):
        return int(time.time()) + int(expires)

    def summd5(self, str):
        m = md5()
        m.update(str)
        return m.hexdigest()

    def sign(self, path, t):
        key = self.time_key
        a = key + self.url_encode(path) + t
        sign_s = self.summd5(a).lower()
        sign_part = "sign=" + sign_s + "&t=" + t
        return sign_part

    def sign_download_url(self, path, expires=1800):
        deadline = self.to_deadline(expires)
        sign_part = self.sign('/%s' % path, self.t16(deadline))
        return '%s/%s?' % (self.host, path) + sign_part


def qiniu_sign_url(hash_key, expires=1800):
    config = Config.QINIU_AUDIOS_CONFIG
    url = QiniuUriGen(**config).sign_download_url(hash_key, expires)
    return url


@cache_for(900)
def qiniu_private_url_gen(key, avinfo=False, md5=False, expires=1800):
    '''七牛私有空间资源下载链接生成器'''
    q = qiniu_auth()
    bucket_host = app.config['QINIU_PRIVITE_HOST']
    base_url = '%s/%s' % (bucket_host, key)
    if avinfo:
        base_url = '%s/%s?avinfo' % (bucket_host, key)
    elif md5:
        base_url = '%s/%s?hash/md5' % (bucket_host, key)
    return q.private_download_url(base_url)


def qiniu_private_avinfo_duration(key):
    '''七牛私有空间音频资源avinfo中duration'''
    private_url = qiniu_private_url_gen(key, avinfo=True)
    duration = get_qiniu_file_duration(private_url)
    return duration


def qiniu_private_avinfo_size(key):
    '''七牛私有空间音频资源avinfo中duration'''
    private_url = qiniu_private_url_gen(key, avinfo=True)
    size = get_qiniu_file_size(private_url)
    return size


def qiniu_private_file_md5(key):
    private_url = qiniu_private_url_gen(key, md5=True)
    req = requests.get(private_url)
    if req.status_code == 200:
        info = req.json()
        return info.get('md5', '')
    return ''


def media_for(hash, scheme=None, style=None):
    if not hash:
        return None
    url = hash.split('!')[0]
    up = urlparse(url)
    hash_domain = up.hostname
    if hash_domain and hash_domain not in Config.QINIU_DOMAINS:
        if hash_domain == 'wx.qlogo.cn':
            hash = hash.replace('http://', 'https://')
        return hash
    _hash = up.path
    if len(_hash) != 0 and _hash[0] == '/':
        _hash = _hash[1:]

    media_host = Config.QINIU_HOST
    url = '%s/%s' % (media_host, _hash)
    if url.endswith('.amr'):
        url = '%s.mp3' % url[:-4]
    if url and style:
        url = '%s!%s' % (url, style)
    return url


def image_for(image, style=None, scheme=None):
    url = media_for(image, scheme=scheme, style=style)
    return url


def get_weixin_media_url(media_id):
    from sub.settings import Config
    from sub.services.wxconfig import get_weixinmp_token
    appid = Config.WEIXINMP_APPID
    url = 'http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s'
    access_token, errors = get_weixinmp_token(appid)
    if errors:
        # TODO 提交到sentry
        return
    media_url = url % (access_token, media_id)
    return media_url


def media_fetch(media_id):
    '''抓取url的资源存储在私有库'''
    media_url = get_weixin_media_url(media_id)
    if media_url:
        auth = qiniu_auth()
        bucket = BucketManager(auth)
        bucket_name = app.config['QINIU_PRIVITE_BUCKET']
        fetch_key = '%s%s.amr' % (media_id, random.randint(1, 1000))
        ret, info = bucket.fetch(media_url, bucket_name, fetch_key)
        if info.status_code == 200:
            # media_saves 转码
            saveas_key = media_saveas(fetch_key)
            if saveas_key:
                return saveas_key
            return fetch_key


def get_media_duration(voice_url):
    """
    :params voice_url: qiniu voice key
    """
    media_url = media_for(voice_url)
    if not media_url:
        return None
    media_url = '%s?avinfo' % media_url
    duration = get_qiniu_file_duration(media_url)
    return duration


def get_media_size(voice_url):
    """
    :params voice_url: qiniu voice key
    """
    media_url = media_for(voice_url)
    if not media_url:
        return None
    media_url = '%s?avinfo' % media_url
    size = get_qiniu_file_size(media_url)
    return size


def get_media_md5(voice_url):
    media_url = media_for(voice_url)
    if not media_url:
        return None
    media_url = '%s?hash/md5' % media_url
    md5 = get_qiniu_file_md5(media_url)
    return md5


def qiniu_auth():
    access_key = str(app.config['QINIU_ACCESS_TOKEN'])
    secret_key = str(app.config['QINIU_SECRET_TOKEN'])
    auth = Auth(access_key, secret_key)
    return auth


def media_saveas(key):
    '''多媒体持久化
       逻辑是：首先去确认私有库中存在key，没有
               则去公有库找，找到就copy一份到私有库，
               公有库也不存在就忽视
    '''
    auth = qiniu_auth()
    bucket = BucketManager(auth)
    private_bucket_name = app.config['QINIU_PRIVITE_BUCKET']
    public_bucket_name = app.config['QINIU_PUBLIC_BUCKET']
    ret, info = bucket.stat(private_bucket_name, key)
    if not ret:
        ret, info = bucket.stat(public_bucket_name, key)
        if ret:
            ret, info = bucket.copy(public_bucket_name, key,
                                    private_bucket_name, key)
    # 转码是使用的队列名称。
    pipeline = 'zaih_media'
    # 要进行转码的转码操作。
    fops = "avthumb/mp3/ab/192k/ar/44100/acodec/libmp3lame"
    # 可以对转码后的文件进行使用saveas参数自定义命名，当然也可以不指定文件会默认命名并保存在当前空间
    saveas_key = "%s.mp3" % key.split('.')[0]
    fops = op_save(fops, private_bucket_name, saveas_key)
    pfop = PersistentFop(auth, private_bucket_name,
                         pipeline, Config.QINIU_NOTIFY_URL)
    ret, info = pfop.execute(key, [fops], 1)
    if ret is not None:
        return saveas_key
