import json
import logging
import consul
import os

LOGS_KEY = "ferris_cli.config"

DEFAULT_CONFIG = os.environ.get('DEFAULT_CONFIG', 'ferris.env')


class ApplicationConfigurator:

    @staticmethod
    def get(config_key):
        return Consul().get(config_key)

    @staticmethod
    def put(config_key, config_value):
        return Consul().put_item(config_key, config_value)


class Consul:

    def __init__(self):
        if os.environ.get('CONSUL_HOST', None):
            self.client = consul.Consul(
                host=os.environ['CONSUL_HOST'],
                port=os.environ['CONSUL_PORT']
            )

    def get_all(self):
        data = {}
        try:
            index, data = self.client.kv.get('', index=None, recurse=True)

            return data
        except Exception as e:
            logging.getLogger(LOGS_KEY).exception(e)

        return data

    def get(self, config_key):
        data = {}

        try:
            index, data = self.client.kv.get(config_key, index=None)

            return json.loads(data.decode('UTF-8'))

        except Exception as e:
            logging.getLogger(LOGS_KEY).exception(e)

        return data

    def delete_item(self, key):
        try:
            self.client.kv.delete(key)

        except Exception as e:
            logging.getLogger(LOGS_KEY).exception(e)

        return

    def put_item(self, key, value):
        try:
            self.client.kv.put(key, value.replace("'", '"'))

        except Exception as e:
            logging.getLogger(LOGS_KEY).exception(e)

        return {key: value}


