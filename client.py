import socket
import sys

# TCP/IPソケット作成
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# ソケットを接続
server_address: str = "./socket.txt"
try:
    sock.connect(server_address)
except socket.error as e:
    print(f"通信に失敗しました: {e}")
    # ソケットを閉じて終了
    sock.close()
    sys.exit(1)

# サーバー接続後、サーバーにメッセージを送信
try:
    message: str = str(input("Enter your message: "))
    # バイト形式に変更
    message_bytes: bytes = message.encode("utf-8")
    # メッセージをサーバーに送信
    sock.sendall(message_bytes)

    # サーバーからの応答待機時間を設定 2秒
    sock.settimeout(2)

    try:
        while True:
            # サーバーからのメッセージを一度に1024バイトずつ受信
            data: bytes = sock.recv(1024)

            # 受信したデータを表示
            if data:
                print(f"Received: {data.decode('utf-8')}")
            # データがない場合はループを抜ける
            else:
                break

    # エラーが発生した場合はエラーメッセージを表示
    except TimeoutError:
        print("Timeout")
finally:
    # ソケットを閉じる
    sock.close()
