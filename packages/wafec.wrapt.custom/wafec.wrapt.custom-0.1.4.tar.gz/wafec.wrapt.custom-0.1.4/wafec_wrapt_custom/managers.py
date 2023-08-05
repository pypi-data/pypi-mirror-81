import requests
import json
import logging

LOG = logging.getLogger(__name__)


class DataEvent(object):
    def __init__(self, source, event_name, value):
        self.source = source
        self.event_name = event_name
        self.value = value


class DataManagerAdapter(object):
    def notify(self, data_event):
        pass


class DataManager(object):
    def __init__(self, api_uri):
        self._api_uri = api_uri

    def notify(self, data_event):
        try:
            data = {
                'source': data_event.source,
                'event_name': data_event.event_name,
                'value': data_event.value
            }
            headers = {
                'Content-Type': 'application/json'
            }
            requests.post(self._api_uri, data=json.dumps(data), headers=headers)
        except Exception as exc:
            LOG.exception(str(exc))
