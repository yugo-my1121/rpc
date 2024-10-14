import socket
import os
import json
import math

# ソケットファイルのパス
SOCKET_PATH = "/tmp/rpc/unix_socket"

def createSocket():
    # 既存のソケットファイルがあれば削除
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    # UNIXソケットの作成
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # ソケットにパスをバインド
    server_socket.bind(SOCKET_PATH)

    return server_socket

def startServer(server_socket):
    # クライアントからの接続を待機
    server_socket.listen(1)
    print(f"Listening on {SOCKET_PATH}")

    while True:
        conn, _ = server_socket.accept()
        print("Client connected")

        # データを受信
        data = conn.recv(1024)
        data = data.decode()

        # json文字列を辞書型で扱えるように変更
        jsonData = json.loads(data)
        result = executionMethod(jsonData['method'],jsonData['params'],jsonData['param_types'])
        print(jsonData['method'])
        print(f"jsonデータ: {jsonData}")
        print(f"result:{result}")

        # 応答データを辞書型で準備
        response = {
            "result": result,
            "id": jsonData['id'],  # クライアントから送られたIDを返す
            "status": "success"  # 任意でステータスも追加可能
        }


        if data:
            # 応答をJSON形式にして送信
            response_json = json.dumps(response)
            conn.sendall(response_json.encode())  # バイナリ形式にエンコードして送信

        conn.close()

def executionMethod(method,params,paramTypes):
    # メソッドの実行
    if method == 'floor':
      result = executionFloor(params)
    elif method == 'nroot':
        result = executionNroot(params[0],params[1])



    return result


def executionFloor(num):
    return math.floor(num)

def executionNroot(x,n):
    return x ** (1 / n)

def main():
    # ソケットの作成とバインド
    newSocket = createSocket()

    # サーバ起動
    startServer(newSocket)


# スクリプト実行時に呼び出し
if __name__ == "__main__":
    main()
