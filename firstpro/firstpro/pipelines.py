# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class MysqlPipeline:

    def open_spider(self, spider):

        self.conn = pymysql.connect(host='localhost', user='root', passwd='123', db='spidernew', port=3306,
                                    charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):


        sql = '''
            insert into qidian(%s) values (%s)
        '''
        fields = ','.join(item.keys())
        value = ','.join(['%%(%s)s' % key for key in item])
        try:
            self.cur.execute(sql % (fields, value),item)
            self.conn.commit()
            print('爬取成功')
        except Exception:
            self.conn.rollback()
        return item

    def close_spider(self, spider):

        self.cur.close()
        self.conn.close()
