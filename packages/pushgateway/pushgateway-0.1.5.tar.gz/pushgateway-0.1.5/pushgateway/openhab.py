from urllib.parse import urljoin
from dataclasses import dataclass
import requests
import sseclient
import json
import threading
import time


@dataclass
class Metadata:
    name: str
    type: str
    readonly: bool


class ServerSentEventStream:

    def __init__(self, openhab_uri: str, itemname: str, on_item_changed_callback):
        self.itemname = itemname
        self.on_item_changed_callback = on_item_changed_callback
        self.openhab_item_event_uri = urljoin(openhab_uri, '/rest/events?topics=smarthome/items/' + itemname + '/state')
        self.is_running = True
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self.__listen)
        self.thread.start()

    def __listen(self):
        while self.is_running:
            try:
                response = requests.get(self.openhab_item_event_uri, stream=True)
                client = sseclient.SSEClient(response)
                try:
                    for event in client.events():
                        data = json.loads(event.data)
                        payload = json.loads(data['payload'])
                        value = payload['value']
                        print("openhab item " + self.itemname + " has been updated to " + str(value))
                        self.on_item_changed_callback(value)
                finally:
                    client.close()
            except Exception as e:
                print("error occurred consuming sse for " + self.itemname + " " + str(e))
                time.sleep(5)

    def stop(self):
        self.is_running = False
        threading.Thread.join(self.thread)


class OpenhabItem:

    def __init__(self, openhab_uri: str, itemname: str):
        self.openhab_uri = openhab_uri
        self.itemname = itemname
        self.openhab_item_uri = urljoin(self.openhab_uri, '/rest/items/' + self.itemname)
        self.__metadata = None
        print("openhab item proxy created for " + itemname + " (item uri " + self.openhab_item_uri + ")")

    def metadata(self) -> Metadata:
        if self.__metadata is None:
            print('openhab item ' + self.name + ' fetching meta data')
            resp = requests.get(self.openhab_item_uri)
            resp.raise_for_status()
            data = json.loads(resp.text)
            type = data['type'].lower()
            readonly = False
            self.__metadata = Metadata(self.name, type, readonly)
            #print('openhab item ' + self.name + " meta data loaded (type: " + self.__metadata.type + ", readonly: " + str(self.__metadata.readonly) + ")")
            print('openhab item ' + self.name + " meta data loaded:  " + str(self.__metadata))
        return self.__metadata

    @property
    def type(self) -> str:
        return self.metadata().type

    @property
    def writeable(self) -> bool:
        return not self.metadata().readonly

    @property
    def name(self) -> str:
        return self.itemname

    @property
    def state(self):
        try:
            resp = requests.get(self.openhab_item_uri + '/state')
            resp.raise_for_status()
            value = resp.text
            print("openhab item " + self.itemname + " read " + str(value))
            return value
        except requests.exceptions.HTTPError as err:
            print("got error by reading openhab item " + self.itemname + " reason: " + resp.text)

    @state.setter
    def state(self, value):
        uri = self.openhab_item_uri + '/state'
        try:
            print("writing openhab item " + self.itemname + " with " + str(value))
            resp = requests.put(uri, data=str(value), headers={'Content-Type': 'text/plain'})
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("got error by writing openhab item " + self.itemname + " = " + str(value) + " using " + uri +  " reason: " + resp.text)

    def new_change_listener(self, on_changed_callback) -> ServerSentEventStream:
        return ServerSentEventStream(self.openhab_uri, self.itemname, on_changed_callback)


