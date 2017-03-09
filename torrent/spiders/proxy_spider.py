#-*-coding:utf-8 -*-
import scrapy
import scrapy_splash
import re
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    
    
    def start_requests(self):
        self.reqidx = 1
        yield scrapy_splash.SplashRequest(url='http://www.kuaidaili.com/proxylist/1/',method='GET',callback=self.parse)
        
    def parse(self, response):
        source = response.body
        # ��������ʽ�����Pattern���� 
        pattern = re.compile(r'((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)).+?(\d+)') 
         
        # ʹ��search()����ƥ����Ӵ�����������ƥ����Ӵ�ʱ������None 
        # ���������ʹ��match()�޷��ɹ�ƥ�� 
        proxys = [];
        for match in re.finditer(pattern,source):
            proxys.append('%s:%s'%(match.group(1),match.group(2)))

        with open('proxys.txt','w') as proxy_file:
            proxy_file.write(','.join(proxys))
        time.sleep(3*60)
        self.reqidx = self.reqidx+1
        yield scrapy_splash.SplashRequest(url='http://www.kuaidaili.com/proxylist/1/#'+str(self.reqidx),method='GET',callback=self.parse)