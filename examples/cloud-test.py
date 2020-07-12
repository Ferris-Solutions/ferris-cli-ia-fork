from cloudevents.sdk.event import v03
import json
from ferris_cli.ferris_cli import CloudEventsAPI
import uuid


data = {}
data['correlationId'] = uuid.uuid1().hex
data['name'] = "john"

event = (
    v03.Event()
    .SetContentType("application/json")
    .SetData(json.dumps(data))
    .SetSource("from-galaxy-far-far-away")
    .SetEventType("cloudevent.greet.you")
)

print(json.dumps(event.Properties()))


print (event.Properties()['source'])
CloudEventsAPI("broker:29092").send(event)

##print(event.GetData()) 