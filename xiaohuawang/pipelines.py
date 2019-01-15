# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os,requests


class XiaohuawangPipeline(object):
    def process_item(self, item, spider):
        # 一个大型项目中可能有多个spider和多个pipeline，判断一下确保item进入对应的pipline中
        if spider.name == 'xiaohua':
            # print(item['folder_name'],item['item_name'].item['img_url'])
            # 创建文件夹
            base_dir = os.path.join(os.path.dirname(__file__) + 'IMG')  # 获取当前脚本所在的路径,双划线表示__file__表示脚本本身，，，__name__ 表示包   拼出来的路径项目根目录
            img_dir = os.path.join(base_dir,item['folder_name'])   # 目录文件名
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
                img_path = os.path.join(img_dir, item['img_name'])     #图片文件名

            # TODO先用同步的方式,scrpay 自带异步请求的方式为作业
            # 请求和保存图片
            img_url = item['img_url']
            resp = requests.get(img_url)
            if resp.status_code == 200:
                img_bytes = resp.content      # 获取二进制
            else:
                print('{}下载失败'.format(img_url))

            # 保存图片
            with open(img_path,mode='wb') as f:
                f.write(img_bytes)
            print('{}保存成功'.format(img_path))










