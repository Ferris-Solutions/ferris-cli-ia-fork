from ferris_cli.ferris_cli import MetricMessage
from ferris_cli.ferris_cli import MetricsAPI
from ferris_cli.ferris_cli import ApplicationConfigurator
from datetime import datetime


# Get a config from consul

configs = ApplicationConfigurator().get('ferris.apps.dataloader.minio-adapter')
print(configs)


# Create and send a MetricMessage

mm = MetricMessage('some_metric',28)
print(mm.toJSON())
mapi = MetricsAPI().send(mm)



