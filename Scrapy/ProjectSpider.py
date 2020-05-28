# -*- coding: utf-8 -*-
import scrapy
import os
import json


class ProjectspiderSpider(scrapy.Spider):
    name = 'ProjectSpider'
    allowed_domains = ['www.instructables.com']
    count = 0
    start_urls = ['https://www.instructables.com/outside/projects/']

    #The following section gathers the headers from various URLs. Comment it and uncomment the line above to undo
    # __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    # links = []
    # with open(os.path.join(__location__, 'out.json')) as links:
    #     links = json.load(links)

    # def start_requests(self):
    #     for i in range(len(self.links["links"])):
    #         yield scrapy.Request('https://www.instructables.com/' + self.links["links"][i]["link"],
    #                              callback=self.parseLinks)

    def parse(self, response):
        links = response.css("a.ible-title::attr(href)").getall()
        next_page = response.css(".arrow-next a::attr(href)").get()
        i = 0
        for link in links:
            i += 1
            yield scrapy.Request('https://www.instructables.com/' + link, callback=self.parseLinks)
        print("next page: " + str(next_page))
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parseLinks(self, response):
        header = response.css("h1.header-title::text").get()
        desc = response.css(".step-body p::text")[0].get()
        desc = (desc[:97] + '...') if len(desc) > 100 else desc
        return {"header": header,
                "desc": desc,
                "link": response.request.url}
