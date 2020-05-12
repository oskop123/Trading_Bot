import json
import socket
import ssl
import time
from threading import Thread

# default connection properites
DEFAULT_ADDRESS = 'xapi.xtb.com'
DEFAULT_PORT = 5124
DEFAULT_STREAMING_PORT = 5125

# max connection tries
API_MAX_CONN_TRIES = 3


# Represents transaction commands
class TransactionSide(object):
    BUY = 0
    SELL = 1


# Represents transaction types
class TransactionType(object):
    ORDER_OPEN = 0
    ORDER_CLOSE = 2


class JsonSocket(object):
    def __init__(self, address, port, encrypt=False):
        if encrypt:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = ssl.wrap_socket(sock)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._address = address
        self._port = port
        self._decoder = json.JSONDecoder()
        self._receivedData = ''

    # server connection
    def connect(self):
        for i in range(API_MAX_CONN_TRIES):
            try:
                self.socket.connect((self._address, self._port))
            except socket.error:
                time.sleep(0.25)
                continue
            return
        raise Exception('Cannot connect to server')

    def _send_obj(self, obj):
        msg = json.dumps(obj)  # serialize dict into JSON format
        if self.socket:
            msg = msg.encode('utf-8')
            self.socket.sendall(msg)  # send data in JSON format
        else:
            raise RuntimeError('socket connection broken')

    def _read(self, bytes_size=4096):
        if not self.socket:
            raise RuntimeError('socket connection broken')
        while True:
            char = self.socket.recv(bytes_size).decode('utf-8')
            self._receivedData += char
            try:
                (resp, size) = self._decoder.raw_decode(self._receivedData)
                if size == len(self._receivedData):
                    self._receivedData = ''
                    break
                elif size < len(self._receivedData):
                    self._receivedData = self._receivedData[size:].strip()
                    break
            except ValueError:
                continue
        return resp

    def _read_obj(self):
        msg = self._read()
        return msg

    def close(self):
        self.socket.close()


class APIClient(JsonSocket):
    def __init__(self, address=DEFAULT_ADDRESS, port=DEFAULT_PORT, encrypt=True):
        super(APIClient, self).__init__(address, port, encrypt)
        self.connect()

    def execute(self, dictionary):
        self._send_obj(dictionary)
        return self._read_obj()

    def disconnect(self):
        self.close()

    def command_execute(self, command_name, arguments=None):
        return self.execute(base_command(command_name, arguments))


class APIStreamClient(JsonSocket):
    def __init__(self, address=DEFAULT_ADDRESS, port=DEFAULT_STREAMING_PORT,
                 encrypt=True, ss_id=None, tick_fun=None):
        super(APIStreamClient, self).__init__(address, port, encrypt)
        self._ssId = ss_id  # stream session id - needed for streaming subscription
        self._tickFun = tick_fun  # data processing function
        self.connect()

        # Thread for reading streaming data
        self._running = True
        self._t = Thread(target=self._read_stream)
        self._t.start()

    def _read_stream(self):
        while self._running:
            msg = self._read_obj()
            self._tickFun(msg)

    def disconnect(self):
        self._running = False  # stop thread function
        self._t.join()  # terminate thread
        self.close()  # close connection

    def execute(self, dictionary):
        self._send_obj(dictionary)

    def subscribe_price(self, symbol, interval):
        self.execute(dict(command='getTickPrices', symbol=symbol, streamSessionId=self._ssId, minArrivalTime=interval))

    def subscribe_prices(self, symbols, interval):
        for symbolX in symbols:
            self.subscribe_price(symbolX, interval)


# return dictionary representing JSON objects
def base_command(command_name, arguments=None):
    if arguments is None:
        arguments = dict()
    return dict([('command', command_name), ('arguments', arguments)])


# return dictionary representing JSON login object
def login_command(user_id, password, app_name=''):
    return base_command('login', dict(userId=user_id, password=password, appName=app_name))
