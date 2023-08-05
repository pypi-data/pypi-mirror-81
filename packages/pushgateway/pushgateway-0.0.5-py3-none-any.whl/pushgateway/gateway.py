from urllib.parse import urljoin
import requests
import os
import pathlib
import websocket
import json
import time
import logging
import threading
import sys


class ValueSync:

    def __init__(self, webthing_uri, webthing_property, openhab_uri, itemname):
        self.logger = logging.getLogger(webthing_property)
        self.webthing_uri = webthing_uri
        self.webthing_property = webthing_property
        self.openhab_uri = openhab_uri
        self.itemname = itemname
        threading.Thread(target=self.__listen).start()

    def __listen(self):
        while True:
            try:
                self.logger.info('connecting webthing ' + self.webthing_property + ' to read meta data..')
                self.openhab_item_uri = urljoin(self.openhab_uri, '/rest/items/' + self.itemname + '/state')
                self.webthing_property_type, self.webthing_readonly, self.webthing_prop_uri, self.webthing_prop_ws_uri = self.__read_metadata(self.webthing_uri, self.webthing_property)
                self.logger.info('webthing property ' + self.webthing_property + " detected (type: " + self.webthing_property_type + ", readonly: " + str(self.webthing_readonly) + ")")

                self.logger.info('reading current state of webthing property ' + self.webthing_property)
                current_state = self.__read_property(self.webthing_prop_uri, self.webthing_property)
                self.__on_webthing_prop_updated(current_state)

                start_time = time.time()
                ws = websocket.WebSocket()
                ws.connect(self.webthing_prop_ws_uri)
                self.logger.info('websocket ' + self.webthing_prop_ws_uri + ' connected')
                try:
                    while (time.time() - start_time) < (10 * 60): # 3 min
                        msg = json.loads(ws.recv())
                        if msg['messageType'] == 'propertyStatus':
                            data = msg['data']
                            if self.webthing_property in data.keys():
                                value = data[self.webthing_property]
                                self.__on_webthing_prop_updated(value)
                finally:
                    self.logger.info('websocket ' + self.webthing_prop_ws_uri + ' disconnected')
                    ws.close()
            except Exception as e:
                self.logger.error("error occured for webthing " + self.webthing_property + ": "+ str(e))
                time.sleep(10)

    def __read_metadata(self, webthing_uri, webthing_property):
        webthing_meta = requests.get(webthing_uri).json()
        webthing_type = webthing_meta['properties'][webthing_property]['type']
        webthing_readonly = webthing_meta['properties'][webthing_property]['readOnly']
        webthing_prop_uri = None
        webthing_prop_ws_uri = None
        for link in webthing_meta['links']:
            if 'rel' in link.keys():
                if link['rel'] == 'properties':
                    webthing_prop_uri = urljoin(webthing_uri, link['href'])
                elif link['rel'] == 'alternate':
                    webthing_prop_ws_uri = urljoin(webthing_uri, link['href'])
        return webthing_type, webthing_readonly, webthing_prop_uri, webthing_prop_ws_uri

    def __read_property(self, webthing_prop_uri, propertyname):
        properties = requests.get(webthing_prop_uri).json()
        return properties[propertyname]

    def __on_webthing_prop_updated(self, new_value):
        item_value = self.convert(new_value, self.webthing_property_type)
        try:
            resp = requests.put(self.openhab_item_uri, data=str(item_value), headers={'Content-Type': 'text/plain'})
            resp.raise_for_status()
            self.logger.info(self.webthing_property + " = " + str(new_value) + " pushed (" + self.webthing_prop_uri + ")")
        except requests.exceptions.HTTPError as err:
            self.logger.error("got error by pushing " + self.webthing_property + " = " + str(new_value) + " to " + self.openhab_item_uri + " reason: " + resp.text)

    def convert(self, propertyvalue, targettype):
        if targettype == 'boolean':
            if propertyvalue:
                return "ON"
            else:
                return "OFF"
        else:
            return propertyvalue


def default_config_file():
    filename = pathlib.Path(os.getcwd(), "gateway.conf")
    if not filename.exists():
        with open(filename, "w") as file:
            file.write("# webthing_root_uri, webthing_property_name, openhab_root_uri, openhab_item_name")
        logging.info("config file " + str(filename) + " generated")
    return str(filename)


def load_config(filename):
    config = list()
    with open(filename, "r") as file:
        for line in file.readlines():
            line = line.strip()
            if not line.startswith("#") and len(line) > 0:
                try:
                    parts = line.split(",")
                    config.append((parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip()))
                except Exception as e:
                    logging.warn("invalid syntax in line " + line + "  ignoring it" + str(e))
    return config


def run(filename):
    for config in load_config(filename):
        ValueSync(config[0], config[1], config[2], config[3])

    while True:
        time.sleep(60)

