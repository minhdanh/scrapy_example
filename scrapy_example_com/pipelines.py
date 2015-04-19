# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
from scrapy_example_com.items   import *


class ScrapyExampleComPipeline(object):
  def __init__(self):
    self.connection = psycopg2.connect(host='localhost', database='scrapy_example_com', user='postgres')
    self.cursor = self.connection.cursor()

  def process_item(self, item, spider):
    # check item type to decide which table to insert
    try:
      if type(item) is CustomerItem:
        self.cursor.execute("""INSERT INTO customers (id, firstname, lastname, phone, created_at, updated_at, state) VALUES(%s, %s, %s, %s, %s, %s, %s)""", (item.get('id'), item.get('firstname'), item.get('lastname'), item.get('phone'),  item.get('created_at'), item.get('updated_at'), item.get('state'), ))
      elif type(item) is CategoryItem:
        self.cursor.execute("""INSERT INTO categories (id, name) VALUES(%s, %s)""", (item.get('id'), item.get('code'), ))
      self.connection.commit()
      self.cursor.fetchall()

    except psycopg2.DatabaseError, e:
      print "Error: %s" % e
    return item

