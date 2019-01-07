#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import time
import uuid
import hmac
import base64
import urllib
from hashlib import sha1
from tornado import gen, httpclient

class AliMail(object):

    config_map = {
        'hangzhou': {
            'regionid': 'cn-hangzhou',
            'host': 'dm.aliyuncs.com',
            'version': '2015-11-23',
        },
        'singapore': {
            'regionid': 'ap-southeast-1',
            'host': 'dm.ap-southeast-1.aliyuncs.com',
            'version': '2017-06-22',
        },
        'sydney': {
            'regionid': 'ap-southeast-2',
            'host': 'dm.ap-southeast-2.aliyuncs.com',
            'version': '2017-06-22',
        }
    }

    def __init__(self, access_id, access_secret, from_address, from_alias, region='hangzhou'):
        if region not in self.config_map:
            raise AliMailException('invalid region')

        self.config = self.config_map[region]
        self.access_id = access_id
        self.access_secret = access_secret
        self.from_address = from_address
        self.from_alias = from_alias

    @gen.coroutine
    def send(self, address, subject, body, is_html=False):
        payload = {
            'Action': 'SingleSendMail',
            'AccountName': self.from_address,
            'ReplyToAddress': 'false',
            'AddressType': 0,
            'ToAddress': address,
            'FromAlias': self.from_alias,
            'ClickTrace': 1,
            'Subject': subject,
        }

        if is_html:
            payload['HtmlBody'] = body
        else:
            payload['TextBody'] = body
        resp = yield self._request(payload)
        raise gen.Return(resp)

    @gen.coroutine
    def _request(self, payload):
        http_client = httpclient.AsyncHTTPClient()
        try:
            parameters = {
                'Format': 'JSON',
                'Version': self.config['version'],
                'AccessKeyId': self.access_id,
                'SignatureMethod': 'HMAC-SHA1',
                'SignatureVersion': '1.0',
                'SignatureNonce': str(uuid.uuid1()),
                'Timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                'RegionId': self.config['regionid'],
            }

            for key in payload.keys():
                parameters[key] = payload[key]

            signature = self._sign(parameters)
            parameters['Signature'] = signature
            url = 'https://%s/?%s' % (self.config['host'], urllib.urlencode(parameters))
            resp = yield http_client.fetch(url)
            raise gen.Return(resp.body)
        except httpclient.HTTPError as e:
            if e.code == 400:
                raise gen.Return(AliMailException(resp))
            else:
                raise gen.Return(e)

    def _sign(self, parameters):
        sorted_parameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        
        canonicalized_querystring = ''
        for (k, v) in sorted_parameters:
            canonicalized_querystring += '&' + self._percent_encode(k) + '=' + self._percent_encode(v)

        string_to_sign = 'GET&%2F&' + self._percent_encode(canonicalized_querystring[1:])    # 使用get请求方法
        h = hmac.new(self.access_secret + "&", string_to_sign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def _percent_encode(self, encode_str):
        encode_str = str(encode_str)
        res = urllib.quote(encode_str.decode('utf-8').encode('utf-8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

class AliMailException(Exception):
    pass
