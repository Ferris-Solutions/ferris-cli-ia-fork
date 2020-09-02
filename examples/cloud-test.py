from cloudevents.sdk.event import v03
import json
from ferris_cli.ferris_cli import CloudEventsAPI
import uuid
import os
import consul
from ferris_cli.ferris_cli import ApplicationConfigurator

from datetime import datetime

def send_direct_loading_event(hdfs_path):

    data = {"file_location": hdfs_path }
    event = (
        v03.Event()
        .SetContentType("application/json")
        .SetData(json.dumps(data))
        .SetEventID("my-id")
        .SetSource("ferris.apps.dataloader.minio-adapter")

        .SetEventType("ferris.dataloader.file_direct_loaded_to_hdfs")
    )

    print(json.dumps(event.Properties()))
    cca = CloudEventsAPI()
    cca.send(event)

def send_confirmation_event(hdfs_path):

    data = {"file_location": hdfs_path }
    event = (
        v03.Event()
        .SetContentType("application/json")
        .SetData(json.dumps(data))
        .SetEventID("my-id")
        .SetSource("ferris.apps.dataloader.minio-adapter")

        .SetEventType("ferris.dataloader.file_loaded_to_hdfs")
    )

    print(json.dumps(event.Properties()))
    broker = ':'.join([platform_environment['KAFKA_BOOTSTRAP_SERVER'],platform_environment['KAFKA_PORT']])
    print(broker)
    cca = CloudEventsAPI()
    cca.send(event)


platform_environment = ApplicationConfigurator().get('ferris.env')
broker = f"kafka://{platform_environment['KAFKA_BOOTSTRAP_SERVER']}:{platform_environment['KAFKA_PORT']}"

dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%Y-%m-%dT%H:%M:%SZ")

print(timestampStr)
send_direct_loading_event('/landing/zone/abc')
send_confirmation_event('/landing/zone/abc')
