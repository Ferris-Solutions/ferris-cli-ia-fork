import json
import uuid
from datetime import datetime
import logging
from cloudevents.sdk.event.v1 import Event

from .broker import FerrisBroker
from .config import ApplicationConfigurator, DEFAULT_CONFIG

LOGS_KEY = "ferris_cli.events"
DEFAULT_TOPIC = 'ferris.events'


class FerrisEvents:

    @staticmethod
    def send(event_type, event_source, data, topic=None, correlation_id=None):

        if not topic:
            topic = ApplicationConfigurator.get(DEFAULT_CONFIG).get('DEFAULT_EVENTS_TOPIC', DEFAULT_TOPIC)

        date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        evt = (
            Event()
            .SetEventID(uuid.uuid1().hex)
            .SetContentType("application/json")
            .SetSource(f"{event_source}")
            .SetEventType(f"{event_type}")
            .SetEventTime(date_time)
            .SetData(json.dumps(data))
        )

        if correlation_id:
            evt.SetSubject(correlation_id)

        try:
            resp = FerrisBroker().send(topic, evt.Properties())

            logging.getLogger(LOGS_KEY).info("Response from broker.send: %s ", str(resp))
        except Exception as e:
            logging.getLogger(LOGS_KEY).error("Error while sending event:")
            logging.getLogger(LOGS_KEY).exception(e)

        return True


