from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.key_exchange_message import EclipsePointResponse, EclipsePointRequest

# --------------------------------------------------------------------------- #
# configure the client logging
# --------------------------------------------------------------------------- #
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x1

# assume a str
R = "refesfwf"*16

def run_sync_client():
    client = ModbusClient('localhost', port=5020)

    # Register key_message to ClientDecoder
    client.register(EclipsePointResponse)

    client.connect()

    log.debug("Send Point")
    rr = client.execute(EclipsePointRequest(R,unit=UNIT))
    log.debug(rr)

    # ----------------------------------------------------------------------- #
    # close the client
    # ----------------------------------------------------------------------- #
    client.close()


if __name__ == "__main__":
    run_sync_client()
