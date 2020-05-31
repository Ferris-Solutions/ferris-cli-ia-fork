from ferris_cli.kafka_handler import MetricMessage
from ferris_cli.kafka_handler import TaskTrackerMessage
from datetime import datetime


# Create a MetricMessage
mm = MetricMessage('sososo',25)
print(mm.toJSON())


# Create a TaskTrackerMessage
dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
print('Current Timestamp : ', timestampStr)
ttm = TaskTrackerMessage('zing','bing','no','STOPPED', 'Long Message',timestampStr,'yooomummuy')
print(ttm.toJSON())