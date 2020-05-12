import time
import xAPIConnector
import data_storage

def main():
    # enter your login credentials here
    user_id = 11096095
    password = "r7vZ9U8vsStd"
    symbols = ('W20', 'DE30')#, 'O2D.DE', 'RRTL.DE', 'RWE.DE', 'UTDI.DE')
    short_window = 10
    long_window = 50

    # create & connect to RR socket
    client = xAPIConnector.APIClient()

    # connect to RR socket, login
    login_response = client.execute(xAPIConnector.login_command(user_id=user_id, password=password))

    # check if user logged in correctly
    if not login_response['status']:
        print('Login failed. Error code: {0}'.format(login_response['errorCode']))
        return

    # get ssId from login response
    ssid = login_response['streamSessionId']

    # create class for data storing
    data = data_storage.DataStorage(symbols, short_window, long_window, client.command_execute)

    def fetch_data(msg):
        print(msg)

    # create & connect to Streaming socket with given ssID
    # and functions for processing ticks, trades, profit and tradeStatus
    sclient = xAPIConnector.APIStreamClient(ss_id=ssid, tick_fun=fetch_data)

    # subscribe for prices of symbols in given interval time
    sclient.subscribe_prices(symbols, 1000)

    # Press 'Enter' to stop
    print('Press Ctrl + C to stop\n')
    input()

    # gracefully close streaming socket
    sclient.disconnect()

    # gracefully close RR socket
    client.disconnect()

if __name__ == "__main__":
    main()