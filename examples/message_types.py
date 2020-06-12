from ferris_cli.ferris_cli import MetricMessage
from ferris_cli.ferris_cli import TaskTrackerMessage
from ferris_cli.ferris_cli import MetricsAPI
from ferris_cli.ferris_cli import TaskTrackerAPI

from ferris_cli.ferris_cli import ApplicationConfigurator





from datetime import datetime


configs = ApplicationConfigurator().get('ferris-template_consul-server-2_1','8500','ferris.apps.dataloader.minio-adapter')
print(configs)

# Create a MetricMessage
mm = MetricMessage('some_metric',28)
print(mm.toJSON())


mapi = MetricsAPI().send('graphite', mm)

#mapi.send_metric('graphite', mm)


# Create a TaskTrackerMessage
dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
print('Current Timestamp : ', timestampStr)
ttm = TaskTrackerMessage('zing','bing','no','STOPPED', 'Long Message',timestampStr,'yooomummuy')
print(ttm.toJSON())

tta = TaskTrackerAPI("broker:29092", "jobstatus")
tta.send(ttm)

