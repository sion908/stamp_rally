# API確認用のクライアント
## 利用方法

1. 拡張機能の導入

[公式リンク](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)を基本的には確認
下記にQiitaからの記事も転記




# 下記[Qiita](https://qiita.com/toshi0607/items/c4440d3fbfa72eac840c)記事からのコピぺ

## VS Code上でHTTPリクエストを送信し、VS Code上でレスポンスを確認できる「REST Client」拡張の紹介


# 概要
* Visual Studio Code（以下VS Code）の拡張機能であるREST Clientが便利だったのでその紹介です。
* 使い方を文字とgifで説明していきます。
* 説明はマーケットプレース以上の情報を足していないので、英語に抵抗がなければ公式ページを照会してください。

# REST Clientとは
VS Code上でHTTPリクエストを送信し、VS Code上でレスポンスを確認できるVS Codeの拡張機能です。

マーケットプレースの[REST Clientのページ](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)でインストールボタンをクリックするか、VS Codeの拡張機能アイコンをクリックして「REST Client」を検索してインストールボタンをクリックするかで使用できます。

文字だけではイメージし辛いかもしれないので、gifで見てみましょう。

左側のタブがリクエスト、右側のタブがレスポンスです。

ブラウザの拡張機能を使うでもなく、ターミナルでたたくでもなく、スタンドアローンなソフトを使うでもなく、エディタ上でリクエスト・レスポンスが完結してしまいます。

しかも、使い方さえ知れば色々な形式のリクエストをテストしたり、設定を読み込んだりできます。

# 使い方
## 基本的なHTTPリクエスト
### GET
```
https://example.com/comments/1
```

Windows: `Ctrl + Alt + R`
Mac: `Cmd + Alt + R`

または

F1 -> `Send Request`

でリクエストを送信できます。

###  POST
```http
POST https://example.com/comments HTTP/1.1
content-type: application/json

{
    "name": "sample",
    "time": "Wed, 21 Oct 2015 18:27:50 GMT"
}
```

Windows: `Ctrl + Alt + R`
Mac: `Cmd + Alt + R`

または

F1 -> `Send Request`

で同様にリクエストを送信できます。リクエストヘッダから1行空けてリクエストボディを書きます。


### 複数行リクエスト
1ファイル内で複数のリクエストを書いておくことができ、 `###` で区切ります。送信したいリクエストのブロックにカーソルを置き、

Windows: `Ctrl + Alt + R`
Mac: `Cmd + Alt + R`

または

F1 -> `Send Request`

でリクエストを送信できます。

同時にリクエストを送信できるというわけではありません。

```http
GET https://example.com/comments/1 HTTP/1.1

###

GET https://example.com/topics/1 HTTP/1.1

###

POST https://example.com/comments HTTP/1.1
content-type: application/json

{
    "name": "sample",
    "time": "Wed, 21 Oct 2015 18:27:50 GMT"
}
```

### リクエスト行
標準通り `メソッド パス名 HTTP/バージョン` の形式です。省略も可能で、メソッドを省略すると `GET` になります。

```http
GET https://example.com/comments/1 HTTP/1.1
```

```
GET https://example.com/comments/1
```

```
https://example.com/comments/1
```

### クエリストリング
こちらも特別なことはないですが、`?`と`&`で改行できます。

```
GET https://example.com/comments?page=2&pageSize=10
```

```
GET https://example.com/comments
    ?page=2
    &pageSize=10
```


### リクエストヘッダー
下記のようにリクエスト行直下から最初の空行まではリクエストヘッダとみなされます。

```
https://example.com/comments/1
User-Agent: rest-client
Accept-Language: en-GB,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4
Content-Type: application/json
```

`User-Agent`を指定しなければ`vscode-restclient`が自動で設定されます。デフォルト値は`rest-client.defaultuseragent`で変更できます。

### リクエストボディ
リクエストヘッダに1行あけて書きます。

```http
POST https://example.com/comments HTTP/1.1
Content-Type: application/xml
Authorization: token xxx

<request>
    <name>sample</name>
    <time>Wed, 21 Oct 2015 18:27:50 GMT</time>
</request>
```

リクエストボディはファイルから読み込むこともできます。

```http
POST https://example.com/comments HTTP/1.1
Content-Type: application/xml
Authorization: token xxx

< ./demo.xml
```

ファイルパスは上記のような相対パスも `< C:\Users\Default\Desktop\demo.xml` のような絶対パスにも対応しています。

### multipart/form-data
こう書きます。

```
POST https://api.example.com/user/upload
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="text"

title
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="image"; filename="1.png"
Content-Type: image/png

< ./1.png
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

## cURLリクエスト
cURLを生で書いて実行することも可能です。ただ、現在サポートされているのは下記のオプションです。

* -X, --request
* -L, --location, --url
* -H, --header(no @ support)
* -b, --cookie(no cookie jar file support)
* -u, --user(Basic auth support only)
* -d, --data, --data-binary

## リクエストをcURLとしてコピーする
REST Client方式で書いたHTTPリクエストからcURL用の文字列を生成できます。

`F1`で検索Windowsを開き、`Copy Request As cURL`を検索してクリックするとcURLのための文字列がクリップボードにコピーされた状態になります。

## リクエストのキャンセル
Windows: `Ctrl + Alt + K`
Mac: `Cmd + Alt + K`

もしくは

F1 -> `Rerun Last Request`

でリクエストをキャンセルできます。


## リクエスト履歴
直近のリクエスト履歴50件を見て、そのリクエストを再送信できます。

Windows: `Ctrl + Alt + H`
Mac: `Cmd + Alt + H`

もしくは

F1 -> `Rerun Last Request`

## レスポンスの保存
レスポンスのタブで画面右上の保存アイコンを選択するとファイルを開くかレスポンスファイルのフルパスをコピーするか選択できます。


保存場所は `/Users/user-name/.rest-client/responses/raw/` フォルダで、拡張子は`http`です。

また、すぐ右隣のアイコンをクリックするとレスポンスのボディだけファイルに保存できます。

保存場所は `/Users/user-name/.rest-client/responses/body/` フォルダで、拡張子は`html`です。

## 認証
Basic認証、Digest認証、SSLクライアント証明書認証に対応しています。

### Basic認証
base64エンコード形式、ユーザ名 + パスワード形式のいずれにも対応しています。

```http
GET https://httpbin.org//basic-auth/user/passwd HTTP/1.1
Authorization: Basic dXNlcjpwYXNzd2Q=
```

```http
GET https://httpbin.org//basic-auth/user/passwd HTTP/1.1
Authorization: Basic user passwd
```

### Digest認証
こう書きます。

```
GET https://httpbin.org/digest-auth/auth/user/passwd
Authorization: Digest user passwd
```

### SSLクライアント証明書認証
`PFX`、`PKCS12`、`PEM`形式の証明書に対応しています。

設定は次のように書きます。

```js
"rest-client.certificates": {
    "localhost:8081": {
        "cert": "/Users/demo/Certificates/client.crt",
        "key": "/Users/demo/Keys/client.key"
    },
    "example.com": {
        "cert": "/Users/demo/Certificates/client.crt",
        "key": "/Users/demo/Keys/client.key"
    }
}
```

`PFX`か`PKCS12`の場合、次のように書きます。

```js
"rest-client.certificates": {
    "localhost:8081": {
        "pfx": "/Users/demo/Certificates/clientcert.p12",
        "passphrase": "123456"
    }
}
```

各設定項目の意味は次の通りです。

* cert: `x509`証明書へのパス
* key: 秘密鍵へのパス
* pfx: `PKCS12`か`PFX`証明書へのパス
passphrase: パスフレーズ（必要な場合のみのオプション）

## 各言語HTTPクライアントコードの生成
組み立てたHTTPリクエストを送信するためのクライアントコードを生成してくれるという機能が付いています。これはびっくりですね！

Windows: `Ctrl + Alt + C`
Mac: `Cmd + Alt + C`

または

F1 -> `Generate Code Snippet`

で言語を選択してください。


## 「HTTP言語」
次の条件を満たすとシンタックスハイライト、コード補完等のサポートが受けられます。

* ファイルの拡張子を`.http`か`.rest`にする
* ファイルの最初の行を[RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html)に基づく`Method SP Request-URI SP HTTP-Version `のフォーマットの標準リクエストにする

## コード補完
下記が対象です。

* HTTP メソッド
+ リクエスト履歴からのHTTP URL
* HTTPヘッダ
* グローバル変数
* 現在の環境/ファイル範囲のカスタム変数
* `Accept` と `Content-Type`ヘッダのMIMEタイプ
* Basic と Digest 方式の認証スキーム

## コードジャンプ
Windows: `Ctrl + Shift + O`
Mac: `Cmd + Shift + O`

または

F1 -> `@`

でリクエストや変数にコードジャンプできます。


## 変数
グローバル変数とカスタム変数をサポートしています。それぞれで同一の変数が定義されている場合、カスタム変数が優先されます。

### カスタム変数
こんな感じでHTTPリクエストと同一のファイル内に書きます。

```
@name = Huachao Mao
@id = 313
@address = Wuxi\nChina

###

@token = Bearer e975b15aa477ee440417ea069e8ef728a22933f0

GET https://example.com/api/comments/1 HTTP/1.1
Authorization: {{token}}

###

PUT https://example.com/api/comments/{{id}} HTTP/1.1
Authorization: {{token}}
Content-Type: application/json

{
    "name": "{{name}}",
    "address": "{{address}}"
}
```

構文は次のとおりです。

* 変数名にスペースを含めてはいけません
* 変数値の先頭と末尾のスペースは無視されます
* エスケープはバックスラッシュ（`\`）を使用します
* 変数はファイル内のどこに書いても大丈夫ですが、リクエストと同じブロック（'###' の中）に書く場合はリクエストとの間に空行が必要です。


### 環境毎に切り替える
設定ファイルを書くことで、環境毎にHTTPリクエストファイル内で読み込む変数を切り替えることができます。

環境の切り替えはエディタの下部の環境名をクリックするか、次のコマンドで切り替えることができます。

Windows: `Ctrl + Alt + E`
Mac: `Cmd + Shift + E`

または

F1 -> `Switch Environment`


設定ファイルは下記のように書きます。

```js
"rest-client.environmentVariables": {
    "$shared": {
        "version": "v1"
    },
    "local": {
        "version": "v2",
        "host": "localhost",
        "token": "test token"
    },
    "production": {
        "host": "example.com",
        "token": "product token"
    }
}
```

`$shared` という変数は全ての環境に適用されますが、上書きできます。

上記設定ファイルに対応するHTTPリクエストは下記のようになります。

```http
GET https://{{host}}/api/{{version}comments/1 HTTP/1.1
Authorization: {{token}}
```

設定場所は*ユーザ設定*ですが、

Windows: `Ctrl + ,`
Mac: `Cmd + ,`

または

F1 -> `ユーザー設定を開く`

でたどれます。



### グローバル変数
あらかじめ定義され、値が動的に変わる変数群です。

次のように使用します。

```
@token = Bearer fake token

POST https://{{host}}/comments HTTP/1.1
Content-Type: application/xml
X-Request-Id: {{token}}

{
    "request_id": "{{$guid}}",
    "updated_at": "{{$timestamp}}",
    "created_at": "{{$timestamp -1 d}}",
    "review_count": "{{$randomInt 5, 200}}"
}
```


`{{$variableName}}`のように使用し、下記が定義されています。

* {{$guid}}: RFC 4122 v4 UUIDを返します
* {{$randomInt min max}}: min以上mac未満のランダムな値を返します
* {{\$timestamp}}: UTC timestampを返します。{{\$timestamp number option}}という形式です。たとえば、3時間前なら{{\$timestamp -3 h}}明後日なら{{$timestamp 2 d}}となります。

{{$timestamp}}のオプションは次のとおりです。

|Option|Description|
|:--|:--|
|y|Year|
|Q|Quarter|
|M|Month|
|w|Week|
|d|Day|
|h|Hour|
|m|Minute|
|s|Second|
|ms|Millisecond|


## レスポンスの見た目の設定
デフォルトでレスポンスはフル（ステータス行、ヘッダ、ボディ）の全てが表示されますが、変更できます。

|Option|Description|
|:--|:--|
|full|デフォルトはこれで、すべてのレスポンスが表示されます|
|headers|ステータス行とヘッダが表示されます|
|body|ボディだけが表示されます|
|exchange|リクエスト・レスポンスの両方が表示されます|


## ユーザー設定

|Option|Description|Default|
|:--|:--|:--|
|rest-client.followredirect|HTTP 3xx レスポンスをリダイレクトとして扱います|true|
|rest-client.defaultuseragent|リクエストヘッダーでUser-Agentヘッダーが省略されている場合、リクエストごとにユーザーエージェントとして追加されます|vscode-restclient|
|rest-client.timeoutinmilliseconds|ミリ秒単位のタイムアウト時間で、0は無制限を表します|0|
|rest-client.showResponseInDifferentTab|レスポンスを別タブで表示します|false|
|rest-client.rememberCookiesForSubsequentRequests|レスポンス時に`Set-Cookie`ヘッダーからCookieを保存し、後続のリクエストに使用します|true|
|rest-client.enableTelemetry|匿名の使用データを送信します|true|
|rest-client.excludeHostsForProxy|プロキシ設定を使用する際除外するホスト|[]|
|rest-client.fontSize|レスポンスプレビューで使用されるフォントサイズをピクセル単位で制御します|13|
|rest-client.fontFamily|レスポンスプレビューで使用されるフォントファミリを制御します|**Menlo**、**Monaco**、**Consolas**、**"Droid Sans Mono"**、**"Courier New"**、**monospace**、**"Droid Sans Fallback"**|
|rest-client.fontWeight|レスポンスプレビューで使用されるフォントの太さを制御します|**normal**|
|rest-client.environmentVariables|環境とカスタム変数を設定します(例 {"production": {"host": "api.example.com"}, "sandbox":{"host":"sandbox.api.example.com"}})|{}|
|rest-client.mimeAndFileExtensionMapping|保存されたレスポンスボディのMIMEタイプとファイル拡張子のカスタムマッピングを設定します|{}|
|rest-client.previewResponseInUntitledDocument|trueに設定されている場合は、無題のドキュメントでレスポンスをプレビューし、それ以外の場合はHTMLビューで表示します|false|
|rest-client.previewResponseSetUntitledDocumentLanguageByContentType|新しいタブで各レスポンスを表示する際にContent-Typeヘッダに基づいてドキュメント言語を自動的に設定します|false|
|rest-client.includeAdditionalInfoInResponse|プレビューが無題のドキュメントを使用するように設定されている場合は、リクエストURLや応答時間などの追加情報を含めます|false|
|rest-client.certificates|異なるホストの証明書パスです。 パスは絶対パスまたは相対パス（ワークスペースまたは現在のhttpファイルから)|{}|
|rest-client.useTrunkedTransferEncodingForSendingFileContent|リクエスト本文としてファイルコンテンツを送信するための転送エンコーディングの使用|true|
|rest-client.suppressResponseBodyContentTypeValidationWarning|レスポンスボディのコンテンツタイプの検証を抑制します|false|
|rest-client.previewOption|レスポンスプレビューの出力オプションです。オプションの詳細は、上記のとおりです|full|

VSCode向けに`http.proxy`と`http.proxyStrictSSL`のプロキシ設定が行われているとそれを反映します。


## 変更履歴
[CHANGELOG](https://github.com/Huachao/vscode-restclient/blob/master/CHANGELOG.md)

## Q&A、issue上げ、コントリビューション
[vscode-restclient](https://github.com/Huachao/vscode-restclient)

* TypeScript: 97.4%
* CSS: 2.6%
