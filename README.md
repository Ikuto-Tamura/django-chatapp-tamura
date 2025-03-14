チャットアプリを丁寧な解説と一緒に実装してみます。

プロジェクト名が、chatapp_pj
アプリ名がchatapp_appです。

本来なら、プロジェクト名にはサービス名、アプリ名には機能名をつけます。

手順書に作成方法を書いています。(随時更新)

スタイリングはGoogleのMaterial Design3を意識して作っています。

アプリを動かす方法

1. クローンする
```
git clone https://github.com/Ikuto-Tamura/django-chatapp-tamura.git
```

2. 必要なパッケージのinstall(仮想環境推奨)をする。
```
pip install -r requirements.txt
```
⚠️注意 requirements.txtが直下にある階層でこのコマンドを実行してください。
cdコマンドとlsコマンドを使いながら階層を移動すると良いです。

3.  migrationを行う

```
python manage.py migrate
```

⚠️注意 manage.pyが直下にある階層でこのコマンドを実行してください。
cdコマンドとlsコマンドを使いながら階層を移動すると良いです。

4.  runserverする

```
python manage.py runserver
```

⚠️注意 manage.pyが直下にある階層でこのコマンドを実行してください。
cdコマンドとlsコマンドを使いながら階層を移動すると良いです。