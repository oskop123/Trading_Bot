import json
import socket
import ssl
import time
from threading import Thread

# connection properites
DEFAULT_ADDRESS = 'xapi.xtb.com'
DEFAULT_PORT = 5124
DEFAULT_STREAMING_PORT = 5125
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
    """ Socket used for JSON communication."""

    def __init__(self, address, port, encrypt=False):
        """ socket - socket object
            _address - destination address (server)
            _port - destination port (server)
            _decoder - object used for decoding JSON
            _receivedData - stores received data"""
        if encrypt:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = ssl.wrap_socket(sock)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._address = address
        self._port = port
        self._decoder = json.JSONDecoder()
        self._receivedData = ''

    def connect(self):
        """ Connect to server. """
        for i in range(API_MAX_CONN_TRIES):
            try:
                self.socket.connect((self._address, self._port))
            except socket.error:
                time.sleep(0.25)
                continue
            return
        raise Exception('Cannot connect to server')

    def _send_obj(self, obj):
        """ Send data to server in JSON format. """

        # serialize dict into JSON format
        msg = json.dumps(obj)
        if self.socket:
            msg = msg.encode('utf-8')
            self.socket.sendall(msg)
        else:
            raise RuntimeError('socket connection broken')

    def _read_obj(self):
        """ Receive data from server. Returns Python dictionary."""
        if not self.socket:
            raise RuntimeError('socket connection broken')
        while True:
            char = self.socket.recv(4096).decode('utf-8')
            self._receivedData += char
            resp = None
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

    def close(self):
        """ Close connection. """
        self.socket.close()


class APIClient(JsonSocket):
    """  Extension of JsonSocket for Request/Response Service. """

    def __init__(self, address=DEFAULT_ADDRESS, port=DEFAULT_PORT, encrypt=True):
        super(APIClient, self).__init__(address, port, encrypt)
        self.connect()

    def execute(self, dictionary):
        """ Sends request. Returns response. """
        self._send_obj(dictionary)
        return self._read_obj()

    def command_execute(self, command_name, arguments=None):
        """ Sends request. Returns response. """
        return self.execute(base_command(command_name, arguments))

    def disconnect(self):
        self.close()


class APIStreamClient(JsonSocket):
    """ Extension of JsonSocket for Streaming Service. """

    def __init__(self, address=DEFAULT_ADDRESS, port=DEFAULT_STREAMING_PORT,
                 encrypt=True, ss_id=None, tick_fun=None):
        super(APIStreamClient, self).__init__(address, port, encrypt)
        """ _ssId -  stream session id 
            _tickFun - data processing function
            _running - loop condition used in _t
            _t - thread used in data receiving process"""
        self._ssId = ss_id
        self._tickFun = tick_fun
        self.connect()
        self._running = True
        self._t = Thread(target=self._read_stream)
        self._t.start()

    def _read_stream(self):
        while self._running:
            self._tickFun(self._read_obj())

    def disconnect(self):
        self._running = False
        self._t.join()
        self.close()

    def execute(self, dictionary):
        """ Sends request. """
        self._send_obj(dictionary)

    def subscribe_price(self, symbol, interval):
        self.execute(dict(command='getTickPrices', symbol=symbol,
                          streamSessionId=self._ssId, minArrivalTime=interval))

    def subscribe_prices(self, symbols, interval):
        for symbolX in symbols:
            self.subscribe_price(symbolX, interval)


def base_command(command_name, arguments=None):
    """ Returns dictionary representing JSON object. """
    if arguments is None:
        arguments = dict()
    return dict([('command', command_name), ('arguments', arguments)])


def login_command(user_id, password, app_name=''):
    """ Returns dictionary representing JSON login object. """
    return base_command('login', dict(userId=user_id, password=password, appName=app_name))
