import os
from elasticsearch import Elasticsearch
import logging
from .config import ApplicationConfigurator, DEFAULT_CONFIG

tracer = logging.getLogger('elasticsearch')
tracer.setLevel(logging.CRITICAL)


class ElasticService:
    index = None
    namespace_key = None
    namespace_value = None

    es_host = conf = ApplicationConfigurator().get().get('ES_HOST')

    def __init__(self, index, namespace_key, namespace_value):
        self.service = Elasticsearch(
            self.es_host
        )
        self.index = index
        self.namespace_key = namespace_key
        self.namespace_value = namespace_value

    def count(self, query=None):
        self.service.indices.refresh(index=self.index)

        body = self._get_body(query)

        json_data = self.service.count(
            index=self.index,
            body=body,
        )

        return int(json_data["count"])

    def get_all(self, offset=0, count=25, query=None, sort_column="@timestamp"):

        data = self.service.search(
            index=self.index,
            body=self._get_body(query),
            size=count,
            from_=offset
        )
        return data["hits"]["hits"]

    def _get_body(self, query=None, sort_column=None):
        if sort_column:

            body = {
                'query': {
                    'match_all': {}
                },
                'sort': [
                    {sort_column: {"order": "desc"}},

                ]
            }
        else:
            body = {
                'query': {
                    'match_all': {}
                },
            }

        if query:
            if self.namespace_value:
                query['bool']['must'].append({
                    "wildcard": {
                        self.namespace_key: f"{self.namespace_value}*"
                    }
                })

            body = {
                'query': query,
            }

        return body
