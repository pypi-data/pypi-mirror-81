import requests


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
        data = {
            'source': data_event,
            'event_name': data_event.event_name,
            'value': data_event.value
        }
        requests.post(self._api_uri, data=data)
