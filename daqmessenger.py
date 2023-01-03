import json
import time
from collections import deque

import stomp
from stomp.exception import ConnectFailedException


class DaqScanListener(stomp.ConnectionListener):
    def __init__(self):
        self.queue = deque()

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        m = json.loads(frame.body)
        self.queue.append(m)


class DaqScanListener4(stomp.ConnectionListener):
    def __init__(self):
        self.queue = deque()

    def on_error(self, headers, message):
        logger.error('Received an error "%s"' % message)

    def on_message(self, headers, message):
        m = json.loads(message)
        self.queue.append(m)


class DaqMessenger:
    def __init__(self, beamline):
        self.beamline = beamline
        self.old_stomp = stomp.__version__[0] == 4

    def connect(self):
        self.conn = stomp.Connection(
            [(self.beamline, 61613)], auto_content_length=False
        )
        if self.old_stomp:
            self.conn.start()
            self.conn.connect()

    def disconnect(self):
        self.conn.disconnect()

    def on_scan(self, message_function, sleep=1):

        dsl = DaqScanListener4() if self.old_stomp else DaqScanListener()
        self.conn.set_listener("scan", dsl)
        self.conn.subscribe(
            destination="/topic/gda.messages.scan", id=1, ack="auto")

        while 1:
            while dsl.queue:
                m = dsl.queue.popleft()
                message_function(m)
            time.sleep(sleep)

    def send_file(self, path):
        message = json.dumps({"filePath": path})
        destination = "/topic/org.dawnsci.file.topic"
        self._send_message(destination, message)

    def send_start(self, path):
        message = json.dumps(
            {"filePath": path, "status": "STARTED", "swmrStatus": "ENABLED"}
        )
        destination = "/topic/gda.messages.processing"
        self._send_message(destination, message)

    def send_update(self, path):
        message = json.dumps(
            {"filePath": path, "status": "UPDATED", "swmrStatus": "ACTIVE"}
        )
        destination = "/topic/gda.messages.processing"
        self._send_message(destination, message)

    def send_finished(self, path):
        message = json.dumps(
            {"filePath": path, "status": "FINISHED", "swmrStatus": "ACTIVE"}
        )
        destination = "/topic/gda.messages.processing"
        self._send_message(destination, message)

    def _send_message(self, destination, message):

        if self.old_stomp:
            self.conn.send(destination, message, ack="auto")
        else:
            self.conn.send(destination=destination, body=message, ack="auto")
