
from conf import SerialConf, OpcConf
from asyncua.common.methods import uamethod
from asyncua import ua, Server
import logging
import asyncio
import serial
import sys
import yaml
sys.path.insert(0, "..")


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


@uamethod
def func(parent, value):
    return value * 2


def read_val(conf):
    with serial.Serial(**conf) as s:
        val = float(s.readline())
    return val


async def main():
    # load configuration files
    serial_conf = SerialConf('pyserver/serial_conf.yml').get_conf()
    _logger.info(f'serial params: {serial_conf}')
    opcua_conf = OpcConf('pyserver/opc_conf.yml').get_conf()

    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint(opcua_conf["endpoint"])

    # setup our own namespace, not really necessary but should as spec
    uri = opcua_conf["uri"]
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    obj = await server.nodes.objects.add_object(idx, opcua_conf["object"])
    var = await obj.add_variable(idx, opcua_conf["variable"], 6.7)
    # Set MyVariable to be writable by clients
    # await var.set_writable()

    # # register testmethod
    # await server.nodes.objects.add_method(
    #     ua.NodeId('ServerMethod', 2),
    #     ua.QualifiedName('ServerMethod', 2),
    #     func,
    #     [ua.VariantType.Int64],
    #     [ua.VariantType.Int64]
    # )

    _logger.info('Starting server!')
    async with server:
        while True:
            await asyncio.sleep(0.1)
            new_val = read_val(serial_conf)
            _logger.info('Set value of %s to %.1f', var, new_val)
            await var.write_value(new_val)

if __name__ == '__main__':
    asyncio.run(main())
