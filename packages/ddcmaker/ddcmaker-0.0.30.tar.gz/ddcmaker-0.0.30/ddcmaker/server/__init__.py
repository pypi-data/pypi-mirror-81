import threading
from ddcmaker.server.http_server.start import http_server
from ddcmaker.server.wss_server.server import wss_server
from ddcmaker.server.wss_server.constant import SERVER_IP, SERVER_PORT, TEST_REGISTER_URL
from ddcmaker.server.wss_server.constant import TEST_UPDATE_URL, PRODUCT_REGISTER_URL, PRODUCT_UPDATE_URL
from ddcmaker.server.wss_server.status import register_maker, update_status


def start_server(debug=False):
    if debug:
        register_url = TEST_REGISTER_URL
        update_url = TEST_UPDATE_URL
    else:
        register_url = PRODUCT_REGISTER_URL
        update_url = PRODUCT_UPDATE_URL

    register_maker(register_url)
    thread = threading.Thread(target=update_status, args=(update_url,))
    thread.setDaemon(True)
    thread.start()

    http_thread = threading.Thread(target=http_server)
    http_thread.start()

    wss_server()
    thread.join()
    http_thread.join()
