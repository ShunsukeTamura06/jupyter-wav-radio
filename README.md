# Jupyter WAVファイルラジオプレーヤー

Jupyter Notebook上で動作するWAVファイルをラジオスタイルで連続再生するためのプログラムです。

## 機能

- 指定ディレクトリ内のWAVファイルを自動検出
- ファイル名でソートされた順に連続再生
- 現在再生中のファイルを視覚的に強調表示
- ループ再生（すべてのファイルの再生後、最初から繰り返し）
- Jupyter Notebook上で完結

## 使用方法

1. このリポジトリをクローンまたはダウンロードする
2. Jupyterで`wav_radio_player.ipynb`を開く
3. WAVファイルのあるディレクトリを`audio_dir`変数で指定する
4. セルを実行して再生開始
5. 停止するには、Jupyterの停止ボタン(■)をクリック

## 必要なライブラリ

- ipywidgets
- IPython
- 標準ライブラリ(glob, os, base64, io, wave, time)

## オプション機能

soundfileライブラリをインストールすることで、より多くの音声フォーマットに対応できます。

```
pip install soundfile
```

コード内のコメントアウトされた部分を有効にして使用してください。

## ライセンス

MIT

---

作成者: ShunsukeTamura06