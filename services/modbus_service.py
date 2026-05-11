
from pymodbus.client import AsyncModbusTcpClient


class ModbusClient:
    def __init__(self, host: str = "localhost", port: int = 502):
        self.host = host
        self.port = port
        self.client = None

    async def _ensure_connected(self):
        if self.client is None:
            self.client = AsyncModbusTcpClient(host=self.host, port=self.port)

        if not self.client.connected:
            await self.client.connect()

        return self.client

    async def _reconnect(self):
        if self.client is not None:
            self.client.close()
        self.client = AsyncModbusTcpClient(host=self.host, port=self.port)
        await self.client.connect()
        return self.client

    async def disconnect(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    async def read_coil(self, address, device_id):
        client = await self._ensure_connected()

        try:
            return await client.read_coils(address, device_id=device_id)
        except Exception as e:
            print("Reconnect because:", e)
            client = await self._reconnect()
            return await client.read_coils(address, device_id=device_id)

    async def write_coil(self, address, value, device_id):
        client = await self._ensure_connected()

        try:
            return await client.write_coil(address, value, device_id=device_id)
        except Exception as e:
            print("Reconnect because:", e)
            client = await self._reconnect()
            return await client.write_coil(address, value, device_id=device_id)

    async def read_registers(self, address, count, device_id):
        client = await self._ensure_connected()

        try:
            return await client.read_holding_registers(address, count=count, device_id=device_id)
        except Exception as e:
            print("Reconnect because:", e)
            client = await self._reconnect()
            return await client.read_holding_registers(address, count=count, device_id=device_id)


modbus_client = ModbusClient()
