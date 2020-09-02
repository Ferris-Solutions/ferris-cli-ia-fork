from ferris_cli.ferris_cli import MetricMessage
from ferris_cli.ferris_cli import MetricsAPI
from ferris_cli.ferris_cli import ApplicationConfigurator
from datetime import datetime
import json


# Get a config from consul

configs = ApplicationConfigurator().get('ferris.apps.dataloader.minio-adapter')
print(configs)

environment = ApplicationConfigurator().get('ferris.env')
print(environment)

dc = {}
dc['something'] = 'test update nothing'

ApplicationConfigurator().put('atest', json.dumps(dc))

# Create and send a MetricMessage

mm = MetricMessage('some_metric',28)
print(mm.toJSON())
mapi = MetricsAPI().send(mm)



