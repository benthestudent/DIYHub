# -*- coding: utf-8 -*-
import scrapy
import os
import json


class ProjectspiderSpider(scrapy.Spider):
    name = 'ProjectSpider'
    allowed_domains = ['makezine.com']
    count = 0
    print("Starting SPider")
    # start_urls = ['https://www.doityourself.com/your-projects/electrical-and-electronics/1',
    #               'https://www.doityourself.com/your-projects/electrical-and-electronics/2']

    #The following section gathers the headers from various URLs. Comment it and uncomment the line above to undo
    # __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    # links = []
    # with open(os.path.join(__location__, 'out.json')) as links:
    #     links = json.load(links)

    def start_requests(self):
        urls = ['https://makezine.com/category/technology/',
                'https://makezine.com/category/home/',
                'https://makezine.com/category/workshop/',
                'https://makezine.com/category/science/',
                'https://makezine.com/category/craft/']
        for url in urls:
            yield scrapy.Request(url,
                                 callback=self.parse)

    def parse(self, response):
        print("Now PaRsing")
        links = response.css(".post a::attr(href)").getall()

        #next_page = response.css(".arrow-next a::attr(href)").get()
        i = 0
        for link in links:
            print("link: " + link)
            i += 1
            yield scrapy.Request(link, callback=self.parseLinks)
        # print("next page: " + str(next_page))
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parseLinks(self, response):
        print("Parsing Links")
        header = response.css(".projects-masthead h1::text").get()
        header = header.replace("\n", "")
        parts = response.css(".parts-tools ul.lists li::text").getall()
        desc = response.css("meta[property='og:description']::attr(content)")[0].get()
        imgPath = response.css("meta[property='og:image']::attr(content)")[0].get()
        desc = (desc[:97] + '...') if len(desc) > 100 else desc
        partArray = []
        for part in parts:
            part = part.replace("\"", "")
            partArray.append(part[:-1])
        return partArray
