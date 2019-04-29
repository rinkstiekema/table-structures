import urllib.parse
import scrapy

from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import re

class aaai(scrapy.Spider):
    name = "aaai_18"

    allowed_domains = ["aaai.org"]
    start_urls = ["https://aaai.org/Library/AAAI/aaai18contents.php"]
    
    def make_dir(self,directory):
        import os
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def parse(self, response):
        for h4 in response.xpath("//h4[text()[contains(.,'AAAI')]]"):
            title = h4.xpath('text()').extract_first()
            title = re.sub(r'AAAI.{2,} Technical Track: ','',title).strip()
            # self.make_dir(title)
            print(title)
            for row in h4.xpath('following-sibling::*'):
                if row.xpath('name()').extract_first() == "h4":
            	    break
                link = row.xpath('comment()').extract_first()
                link = link.replace('<!--','').replace('-->', '')
                commentsel = Selector(text=link, type="html")
                pdf = commentsel.xpath('//a/@href').extract_first()
                pdf = pdf.replace('view','download')
                yield Request(
                    url=pdf,
                    callback=self.save_pdf,
                    meta={'title': title}
                )

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        with open(path+".pdf", 'wb') as f:
            f.write(response.body)


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(aaai)
    process.start()