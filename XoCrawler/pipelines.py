# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.count = 0
        self.file = codecs.open('scraped_data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        line = json.dumps(
            dict(item),
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )

        if self.count != 0:
            line = ",\n" + line
        else:
            self.count = 1

        self.file.write(line)
        return item

    def open_spider(self, spider):
        self.file = codecs.open('scraped_data_utf8.json', 'w', encoding='utf-8')
        self.file.write("[")

    def close_spider(self, spider):
        self.file.write("]")
        self.file.close()

class XocrawlerPipeline(object):
    def process_item(self, item, spider):
        return item
