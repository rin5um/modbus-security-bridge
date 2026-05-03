# 研究目的のみ、ホストオンリーの環境でのみ使用

import socket
import threading

LISTEN_HOST = '0.0.0.0'          # どのNICでもOKという意味, 要は使用するNICのIPアドレス
LISTEN_PORT = 502
VALVE_HOST = '192.168.95.10'     # どことconnectするかで使用するからバルブのIPアドレス
VALVE_PORT = 502

# 正常な送信元IPのリスト, PLCのIPアドレス
ALLOWED_IPS = ['192.168.95.2']


# inspect関数はどのようなフィルタリングルールを定義している
def inspect(data, src_ip):
    # パケットが短すぎる場合は通す
    if len(data) < 8:
        return True

    # 1. 送信元IPチェック, Attack_demonstration.pyは送信元がkaliのIPアドレスなのでこれで遮断できる
    if src_ip not in ALLOWED_IPS:
        print(f'[BLOCKED] Unauthorized IP: {src_ip}')
        return False

    fc = data[7]  # ファンクションコード, Wiresharkの Modbus TCP以上の値がdataに格納される 右下の画面と対応を考えればわかる

    # 2. FC6 (Single Register Write) のチェック
    if fc == 6:
        value = int.from_bytes(data[10:12], 'big')
        if value >= 60000 or value == 0:
            print(f'[BLOCKED] FC6 abnormal value: {value}')
            return False
        print(f'[ALLOW] FC6 value: {value}')

    # 3. FC16 (Multiple Registers Write) のチェック
    elif fc == 16:
        print(f'[ALLOW] FC16 detected from {src_ip}')
        return True

    # 4. FC4 (Read Input Registers) などの読み取り専用パケット
    else:
        # 読み取り命令は基本的に無害なので通す
        return True

    return True


def handle_connection(conn, addr):
    src_ip = addr[0]
    
    # 誰が接続してきたかのログを標準出力する
    print(f'[INFO] Connected from {src_ip}')

    # バルブへの接続, try-exceptは例外処理, except 例外型: 例外型と同じ例外発生時の処理
    try:
        valve_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        valve_sock.connect((VALVE_HOST, VALVE_PORT))
        
        # ExceptionはZeroDivisionError等のあらゆる例外型を総括した例外型, eと一旦名付ける必要がある
    except Exception as e:
        print(f'[ERROR] Cannot connect to Valve: {e}')
        # 例外が発生したらスレッドを終了する
        conn.close()
        return

    try:
        while True:
            # 4096byteのデータをdataに格納, ページサイズが4096だから 2の冪乗をよく使う
            data = conn.recv(4096)
            
            # dataが空だったら通信を終わる
            if not data:
                break

            print(f'[RECV] {data.hex()}')

            if not inspect(data, src_ip):
                # パケットを捨てて次を待つ（接続は維持）, inspect関数の戻り値がFalseならif文を実行, Valveへ転送しない
                continue

            # Valveへ転送
            valve_sock.sendall(data)

            # Valveからのレスポンスを受け取るまで待ち状態 その後、PLCへ返す
            response = valve_sock.recv(4096)
            conn.sendall(response)

    except Exception as e:
        print(f'[ERROR] {e}')
    finally:
        conn.close()
        valve_sock.close()
        print(f'[INFO] Connection closed: {src_ip}')


def main():
    # AF_INEFT : IPv4プロトコルファミリー, SOCK_STREAM : TCPソケット
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # KaliのどのNIC(0.0.0.0)に届いたものでもok, 宛先ポート番号502のパケットならね
    server_sock.bind((LISTEN_HOST, LISTEN_PORT))
    
    # ソケットを接続待ち状態にする
    server_sock.listen(5)
    
    # 
    print(f'[INFO] Bridge listening on port {LISTEN_PORT}')
    print(f'[INFO] Forwarding to Valve: {VALVE_HOST}:{VALVE_PORT}')

    while True:
        # 通信が来るまでブロッキング, connに新しいソケットを, addrに送信元(PLC)IPアドレスを格納
        conn, addr = server_sock.accept()
        
        # 接続ごとに分身(スレッド)を作って処理する, Threadメソッドの第一引数はやらせたい仕事を, 
        # 第二引数はhandle_connection関数に必要な2個の引数をタプルで渡す
        thread = threading.Thread(target=handle_connection, args=(conn, addr))
        
        # 本体が終了したら一緒に死んでいいよ, start()メソッドでスレッドが別の時間軸で動き出す
        thread.daemon = True
        thread.start()


if __name__ == '__main__':
    main()
