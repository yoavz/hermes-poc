# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class HermesItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class DealnewsItem(Item):
    id = Field()
    title = Field()
    price = Field()
    tags = Field()
    url = Field()

class EbayItem(Item):
    id = Field()
    title = Field()
    price = Field()
    tags = Field()
    url = Field()

class DizbeeItem(Item):
    title = Field()
    price = Field()
    tags = Field()
    url = Field()
