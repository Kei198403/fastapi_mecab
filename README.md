# プロジェクト構築

Dev Containersの環境ができていれば、リポジトリをクローンして、VS Codeで開けば使える状態になります。

```
git clone https://github.com/Kei198403/fastapi_mecab.git
```

# 環境情報
- Python：3.11
- パッケージ管理： poetry
- Linter: flake8、mypy
- Formatter: autopep8
- MeCab: インストール済みの前提。バージョンは0.996。
- CaboCha: インストール済みの前提。バージョンは0.69。

.devcontainer/Dockerfileで指定しているイメージのバージョンを変更すれば、別のバージョンでも利用できるはずです。  

docker imageは、「kei198403/mecab-neologd-py3:3.11」を使用。

## Dev Containersの環境でのアプリ実行

### make dev

live reloadありでuvicornを実行。

### make start

live reloadなしでuvicornを実行。

# venv環境について

プロジェクトルート直下に.venvディレクトリを作るようになっています。  
Dev Containersで開いた際、.devcontainer/init.shでpoetry installを実行しています。  
なお、初回はパッケージインストールより前にunittestのDiscoverが動いてエラーが出ることがありますが、
パッケージのインストールが終われば正常にテストができるようになります。

venv環境をリセットする場合は、.venvを削除してコンテナをリビルドしてください。

## venvの設定(poetry config --list)
- virtualenvs.options.always-copy: true  
  WindowsのWSL+Docker+Dev Containers環境で、.venv内にシンボリックリンクが含まれていて、Windowsおよびwslからアクセスできない場合、Dev Containers環境が起動しなくなる問題を回避するため、シンボリックリンクを作らないようにファイルをコピーする。
- virtualenvs.in-project: true  
  プロジェクト内に.venvを作成する。.vscode/settings.jsonでの各種ツールのパスを固定化するため。
- virtualenvs.options.system-site-packages: true  
  システムのsite-packageにインストールしているMeCabとCaboChaのライブラリをvirtualenv環境でもアクセスできるようにするため。

# GitコミットのPrefixルール

- feat: 新しい機能
- fix: バグの修正
- doc: ドキュメントのみの変更
- style: 空白、フォーマット、セミコロン追加など
- refactor: 仕様に影響がないコード改善(リファクタ)
- perf: パフォーマンス向上関連
- test: テスト関連
- chore: ビルド、補助ツール、ライブラリ関連
- deps: 非推奨へ変更
- revert: 切り戻し

参考：https://pypi.org/project/git-changelog/
参考：https://qiita.com/numanomanu/items/45dd285b286a1f7280ed

# Poetryコマンドリファレンス

| コマンド | 備考 |
| ---- | ---- |
| poetry shell | venv環境へ接続 |
| poetry config --list | poetryの設定一覧を表示 |
| poetry add パッケージ | パッケージを追加 |
| poetry add -G dev パッケージ | 開発パッケージを追加 |
| poetry show | パッケージを表示 |
| poetry show --outdated | アップデート可能なパッケージを表示 |
| poetry update --dry-run | アップデート処理の仮実行 |
| poetry update パッケージ | 特定のパッケージを更新 |
| poetry update | アップデートの実行 |
| poetry shell | venv環境をアクティベートする |
| poetry install | dependencies、dev-dependenciesをインストール |
| poetry install --no-dev | dependenciesのみをインストール |
| poetry check | pyproject.tomlの検証 |
| poetry env info | venv環境情報を表示 |

ドキュメント：https://python-poetry.org/docs/

# Dev Containersについて

[VS CodeでDocker開発コンテナを便利に使おう](https://qiita.com/Yuki_Oshima/items/d3b52c553387685460b0)

