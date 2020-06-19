# -*- coding: utf-8 -*-
import scrapy
import os
import json


class ProjectspiderSpider(scrapy.Spider):
    name = 'PartSpider'
    allowed_domains = ['sparkfun.com']
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
        baseURL = "https://www.sparkfun.com/products/"
        for i in range(0, 500):
            url = baseURL + str(i) + ".json"
            yield scrapy.Request(url,
                                 callback=self.parse)

    def parse(self, response):
        print("Now PaRsing")
        partJSON = json.loads(response.text)
        name = partJSON["name"]
        categories = partJSON["categories"]
        catStr = ""

        for cat in categories:
            cstring = str(cat).replace("{", "")
            cstring = cstring.replace("}", "")
            cstring = cstring.replace("'", "")
            cstring = cstring.split(": ")[1]
            catStr += cstring + ","
        catStr = catStr[:-1]
        print(catStr)
        return {"name": name, "categories": str(catStr)}
