# PyTest の実行

```shell
./run.sh doc pytest
```
or  
実行するテストを指定したい場合
```shell
./run.sh doc pytest tests/unit/test_routeguide_client.py::TestRouteGuideClient::test_init_RouteGuideClient
./run.sh doc pytest {ファイル名}::{クラス名}::{テスト名}
```

# PyTest の書き方

1. それぞれの関数で用いている外部 API の mock(patch_get など)を作成する。
2. 以下のような形で、mock を適用する。

```python
    mocker.patch("services.hoge.get", side_effect=patch_get)
```

3. await async_client.get で API を叩き、結果を取得し、期待する結果かどうかを試す。
