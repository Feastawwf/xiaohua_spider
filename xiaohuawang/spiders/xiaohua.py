# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector    #路径
from scrapy.http import Request         # 银如意request
from xiaohuawang.items import XiaohuawangItem


class XiaohuaSpider(scrapy.Spider):
    name = 'xiaohua'
    allowed_domains = ['xiaohuar.com']
    start_urls = ['http://www.xiaohuar.com/hua']

    # 自定义头部
    custom_settings = {
            'DEFAULT_REQUEST_HEADERS' : {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh',
            'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 71.0.3578.98Safari / 537.36',
        }
    }

    # 存放待爬取的url
    url_set = set()

    def parse(self, response):
        """
        请求首页图集列表后得到列表页，解析每个图集详情页的地址
        """

        a_list = Selector(response).xpath("//div[@class='img']/a")
        for a in a_list:
            detail_url = a.xpath('.//@href').extract_first()
            if detail_url in self.url_set:
                pass

            else:
                # 添加到待爬取链接池
                self.url_set.add(detail_url)
                # 发现 画廊页 url  和详情页  路由存在规律，可以直接转换，节省一次requests请求和xpath解析
                gallery_url = detail_url.replace('/p','/s')
                # yield相当于同步函数里的返回值，callback相当于方法嵌套调用，只不过这两个关键字表现异步处理过程，yield生成请求对象（还没有发送请求）到列中，框架从队列中取一个请求对象去请求，得到响应后再交给回调函数处理。
                yield Request(url=gallery_url,callback=self.img_parse)  # callback交给下一级引用,回调函数

    def img_parse(self,response):
        # '//div[@class="inner"]/a/img/@src'
        """解析请求画廊页的html结果，生成item"""
        src_list = Selector(response).xpath('//div[@class="inner"]/a/img/@src').extract()
        folder_name=Selector(response).xpath('//h1/text()').extract_first()

        for src in src_list:
            print('图片资源',src)
            img_url = src
            if img_url.startswith('https'):
                pass
            else:
                # 路由形成，协议http，没有解析xiaohuar.com
                img_url = 'http://www.xiaohuar.com'

            img_name = src.split('/')[-1]    # 分隔取最后一项负1

            # item = XiaohuawangItem(folder_name=folder_name,img_name=img_name,img_url=img_url)

            item =XiaohuawangItem()
            item['folder_name'] = folder_name
            item['img_name'] = img_name
            item['img_url'] = img_url
            yield item





