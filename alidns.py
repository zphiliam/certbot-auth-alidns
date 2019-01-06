#!/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from config import *
import json
from sys import argv
# client = AcsClient('<accessKeyId>', '<accessSecret>', 'cn-hangzhou')

client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, 'nothing')


class AliDNS(object):

    def __init__(self, domain_name=''):
        self.domain_name = domain_name

    def add_domain_record(self, rr, value, type='TXT'):
        # https://help.aliyun.com/document_detail/29772.html?spm=a2c4g.11186623.6.647.5fce1ba8XGwW3b
        # https://api.aliyun.com/?spm=a2c1g.8271268.10000.1.751edf252XRbqs#product=Alidns&api=AddDomainRecord&params={}&tab=DEMO&lang=PYTHON
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('alidns.aliyuncs.com')
        request.set_method('POST')
        request.set_version('2015-01-09')
        request.set_action_name('AddDomainRecord')

        request.add_query_param('Type', type)
        request.add_query_param('RR', rr)
        request.add_query_param('DomainName', self.domain_name)
        request.add_query_param('Value', value)

        response = client.do_action(request)
        print(response.decode('utf-8'))

    def describe_domain_records(self):
        # https://help.aliyun.com/document_detail/29751.html?spm=a2c4g.11186623.6.627.30e77d8cBvKO4T
        # https://api.aliyun.com/?spm=a2c1g.8271268.10000.1.751edf252XRbqs#product=Alidns&api=DescribeDomainRecords&params={}&tab=DEMO&lang=PYTHON
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('alidns.aliyuncs.com')
        request.set_method('POST')
        request.set_version('2015-01-09')
        request.set_action_name('DescribeDomainRecords')

        request.add_query_param('DomainName', self.domain_name)
        request.add_query_param('PageNumber', '1')
        request.add_query_param('PageSize', '500')
        response = client.do_action(request)
        rs = response.decode('utf-8')
        # print(response.decode('utf-8'))
        # print(str(response, encoding='utf-8'))
        data = json.loads(rs)
        return data

    def delete_domain_record(self, record_id):
        # https://help.aliyun.com/document_detail/29773.html?spm=a2c4g.11186623.6.648.4bc76e00EoOIru
        # https://api.aliyun.com/?spm=a2c1g.8271268.10000.1.751edf252XRbqs#product=Alidns&api=DeleteDomainRecord&params={}&tab=DEMO&lang=PYTHON
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('alidns.aliyuncs.com')
        request.set_method('POST')
        request.set_version('2015-01-09')
        request.set_action_name('DeleteDomainRecord')

        request.add_query_param('RecordId', record_id)

        response = client.do_action(request)
        # print(response.decode('utf-8'))

    def update_domain_record(self, rid, rr, value, type='TXT'):
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('alidns.aliyuncs.com')
        request.set_method('POST')
        request.set_version('2015-01-09')
        request.set_action_name('UpdateDomainRecord')

        request.add_query_param('RecordId', rid)
        request.add_query_param('RR', rr)
        request.add_query_param('Type', type)
        request.add_query_param('Value', value)

        response = client.do_action(request)
        # print(str(response, encoding='utf-8'))


if __name__ == '__main__':

    # import time
    # domain = 'iot-c.top'
    # acme_challenge = 'test.z'
    # validation = str(time.time())

    print(argv)
    file_name, domain, acme_challenge, validation = argv

    # 支持二级以上通配符
    words = domain.split('.')
    if len(words) > 2:
        domain = ".".join(words[-2:])
        acme_challenge = acme_challenge + "." + ".".join(words[:-2])

    dns = AliDNS(domain)

    # 列出所有解析记录
    data = dns.describe_domain_records()
    # print(json.dumps(data, indent=2))

    record_list = data["DomainRecords"]["Record"]
    # print(len(record_list))

    if record_list:
        for item in record_list:
            if acme_challenge == item['RR']:
                # 删除原有的记录
                dns.delete_domain_record(item['RecordId'])
    print("阿里云DNS添加 TXT 记录：\n"
          "{} --> {}".format(acme_challenge + "." + domain, validation))

    # 添加新记录
    dns.add_domain_record(acme_challenge, validation)
