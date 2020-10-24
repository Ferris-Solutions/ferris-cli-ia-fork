#!/usr/bin/env python
import faust
import json
from random import random
from kafka import KafkaProducer
import os
import consul
from datetime import datetime
from elasticsearch import Elasticsearch

import logging
from jsonformatter import JsonFormatter

import jinja2

print('done')

es = Elasticsearch(hosts='http://elasticsearch:9200',verify_certs=False)




time_from = "2020-08-27T11:47:09Z"
time_to = "2020-08-30T11:47:09Z"
start_from = 0
result_size = 20
metric_type = "ferris.dataloader.*"  


templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "query_template.jinja"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(time_from=time_from,time_to=time_to,
	start_from=start_from,result_size=result_size,metric_type=metric_type) 

print(outputText)


res = es.search(index="ferris-events", body=outputText)

print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print(hit["_source"])
    #print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

print('done')

 
                 

                     