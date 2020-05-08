import xAPIConnector
import data_storage
import time

def main():
    # enter your login credentials here
    user_id = 11096095
    password = "r7vZ9U8vsStd"
    symbols = ('EURUSD', 'EURGBP', 'EURJPY')
    short_window = 10
    long_window = 40

    # create & connect to RR socket
    client = xAPIConnector.APIClient()

    # connect to RR socket, login
    login_response = client.execute(xAPIConnector.loginCommand(userId=user_id, password=password))

    # check if user logged in correctly
    if not login_response['status']:
        print('Login failed. Error code: {0}'.format(login_response['errorCode']))
        return

    # get ssId from login response
    ssid = login_response['streamSessionId']

    # create class for data storing
    data = data_storage.DataStorage(symbols, short_window, long_window, client.commandExecute)

    # create & connect to Streaming socket with given ssID
    # and functions for processing ticks, trades, profit and tradeStatus
    sclient = xAPIConnector.APIStreamClient(ssId=ssid, tickFun=data.fetch_data)

    # subscribe for prices
    sclient.subscribePrices(symbols)

    # this is an example, make it run for 5 seconds
    time.sleep(9999)

    # gracefully close streaming socket
    sclient.disconnect()

    # gracefully close RR socket
    client.disconnect()
