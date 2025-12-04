"""
APIのI/O定義を行う
そこまでかもしれない

命名規則:
クエリ（処理）の名前 + 接尾語

1.リクエストモデル: "Request"
                ex. UserCreateRequest: ユーザーの作成要求

2.レスポンスモデル: "Response"
                ex. UserResponse: ユーザー情報の応答

3.アウトプットモデル: "Output"
                ex. UserListOutput: 複数のユーザー情報のリスト

4.エラーモデル: "Error"
                ex. UserCreateError: ユーザー作成中に発生したエラー

レスポンスモデルはエンドポイント全体の応答データのフォーマットを定義
アウトプットモデルはエンドポイント内の特定の処理段階で生成されるデータを定義

"""
