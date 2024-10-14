const net = require('net');
//ソケットパス
const path = '/tmp/rpc/unix_socket';


//jsonファイル読み込み
const jsonData = require('./request.json');

//ソケット接続
const client = net.createConnection(path, () => {
    console.log('Connected to server.');

    // JSONデータをサーバに送信
    const jsonString = JSON.stringify(jsonData);
    client.write(jsonString);
});


//データをサーバから受信した時
client.on('data', (data) => {
  console.log('返却データ:' + data.toString());//データを文字列に変換
  client.end();//接続を終了する
});

//接続終了したら
client.on('end', () => {
  console.log('disconnected from server');
});
