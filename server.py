import os
import socket

from faker import Faker

# Fakerインスタンスを作成
# これにより、ランダムな名前を生成できるようになる
fake = Faker()

# UNIXソケットをストリームモードで作成
sock: socket.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# サーバーが使用するソケットファイルのパス
socket_address: str = "./socket.txt"

# ソケットファイルが存在する場合は削除する
try:
    os.unlink(socket_address)
# ソケットファイルが存在しない場合は何もしない
except FileNotFoundError:
    pass

# サーバーアドレスにソケットをバインドする
sock.bind(socket_address)

# 接続要求を待つ
sock.listen(1)

# クライアントからの接続を受け入れ続ける
while True:
    # クライアントからの接続を受け入れる
    connection, client_address = sock.accept()
    try:
        while True:
            # 一度に1024バイトずつデータを受信
            data: bytes = connection.recv(1024)
            # データがある場合は受信したデータを表示
            if data:
                print(f"受信したメッセージ: {data.decode('utf-8')}")

                # クライアントに返すメッセージ作成
                response_message_name: str = fake.name()
                response_message_age: int = fake.random_int(min=1, max=100)
                response_message_address: str = fake.address().replace("\n", ", ")
                # 返信をクライアントに送信
                connection.sendall(response_message_name.encode("utf-8") + b"\n")
                connection.sendall(str(response_message_age).encode("utf-8") + b"\n")
                connection.sendall(response_message_address.encode("utf-8") + b"\n")
            # データがない場合はループを抜ける
            else:
                break
    finally:
        # 接続を閉じる
        connection.close()
        break  # ループを抜けて次の接続を待つ
# すべての処理が終わったらソケットを閉じる
sock.close()
