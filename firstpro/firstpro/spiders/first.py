import scrapy
from copy import deepcopy


class FirstSpider(scrapy.Spider):
    name = 'first'
    # allowed_domains = ['www.xx.com']
    start_urls = ['https://www.qidian.com/all?vip=0']

    def parse(self, response, **kwargs):
        li_list = response.xpath('//div[@class="work-filter type-filter"]//li[@data-id>0]')
        for li in li_list:
            item = {}
            item['cate_url'] = response.urljoin(li.xpath('./a/@href').extract_first())
            item['cate'] = li.xpath('./a/text()').extract_first()
            yield scrapy.Request(
                url=item['cate_url'],
                callback=self.parse_book_list,
                meta={"item": deepcopy(item)}
            )

    def parse_book_list(self, response):
        item = deepcopy(response.meta['item'])

        li_list = response.xpath('//div[@class="book-img-text"]//li[@data-rid>0]')
        for li in li_list:
            item['book_img'] = response.urljoin(li.xpath('./div[1]/a/img/@src').extract_first())
            item['book_url'] = response.urljoin(li.xpath('./div[1]/a/@href').extract_first())
            item['book_name'] = li.xpath('./div[2]/h4/a/text()').extract_first()
            item['book_author'] = li.xpath('./div[2]/p[1]/a/text()').extract_first()
            item['book_status'] = li.xpath('./div[2]/p[1]/span/text()').extract_first()
            item['book_desc'] = li.xpath('./div[2]/p[2]/text()').extract_first().strip()

            yield item
        # 翻页
        next_url = response.xpath('//ul[@class="lbf-pagination-item-list"]/li[last()]/a/@href').extract_first()
        if next_url != "javascript:;":
            next_url = response.urljoin(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_book_list,
                meta={"item":item}
            )