# python-template

VS Code+Remote ContainerでのPython環境のテンプレートプロジェクト。

# Remote Containerについて

[VS CodeでDocker開発コンテナを便利に使おう](https://qiita.com/Yuki_Oshima/items/d3b52c553387685460b0)

# プロジェクト構築

Remote Containerの環境ができていれば、リポジトリをクローンして、VS Codeで開けば使える状態になります。

```
git clone https://github.com/Kei198403/python-template.git
```

# テンプレートの環境情報
- Python：3.9.5
- パッケージ管理： poetry
- Linter: flake8、mypy
- Formatter: autopep8

.devcontainer/Dockerfileで指定しているイメージのバージョンを変更すれば、別のバージョンでも利用できるはずです。  
なお、pyproject.tomlでpython = "^3.9"が指定されているので、3.9以前のバージョンを利用する場合はこちらも修正が必要になります。

# venv環境について

プロジェクトルート直下に.venvディレクトリを作るようになっています。  
Remote Containerで開いた際、.devcontainer/init.shでpoetry installを実行しています。  
なお、初回はパッケージインストールより前にunittestのDiscoverが動いてエラーが出ることがありますが、
パッケージのインストールが終われば正常にテストができるようになります。

venv環境をリセットする場合は、.venvを削除してコンテナをリビルドしてください。

## GitコミットのPrefixルール

- feat: 新しい機能
- fix: バグの修正
- docs: ドキュメントのみの変更
- style: 空白、フォーマット、セミコロン追加など
- refactor: 仕様に影響がないコード改善(リファクタ)
- perf: パフォーマンス向上関連
- test: テスト関連
- chore: ビルド、補助ツール、ライブラリ関連

参考：https://qiita.com/numanomanu/items/45dd285b286a1f7280ed

## Poetryコマンドリファレンス

| コマンド | 備考 |
| ---- | ---- |
| poetry shell | venv環境へ接続 |
| poetry config --list | poetryの設定一覧を表示 |
| poetry add パッケージ | パッケージを追加 |
| poetry add -D パッケージ | 開発パッケージを追加 |
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
