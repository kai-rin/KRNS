# KRNS LoRA/LyCORIS file renamer | KRNS LoRA/LyCORIS ファイルリネーマー

KRNS - Known for Rarity, Niche &amp; Specialized

## 概要

Stable DiffusionのLoRA/LyCORIS保管ディレクトリが永遠にごちゃごちゃしてる&Civitaiからダウンロードするファイル名がわりと無秩序なので作りました。KRNS LoRA/LyCORIS ファイルリネーマーはPythonとPyQt5で作られた、LoRA/LyCORISファイルを一括でリネームするGUIを持つツールです。

## 機能

### ディレクトリ選択

`Select Directory`をクリックして、LoRA/LyCORISがたまってるディレクトリを選びましょう。

### LoRA/LyCORIS ファイルリネーマー

1. **モデルIDをファイル名の先頭に追加**: たとえば `AwyHandHeartXL.safetensors` を `126227_AwyHandHeartXL.safetensors` に変えます。 ここの `126227` はCivitaiのモデルページを開いたときにURLに表示されている数字と同一です。同じモデルページのバージョン違いのLoRA/LyCORISの場合でも、同じ番号を付与してしまいます。

2. **モデルIDを新しい基本ファイル名として使用**: `AwyHandHeartXL.safetensors` をシンプルに `126227.safetensors` にします。同じモデルページのバージョン違いのLoRA/LyCORISの場合、同じ番号に変換してしまいます。あんまりよろしくないですね！（そのうち改良するかも。）

3. **ファイル名を元に戻す**: モデルIDをファイル名の先頭に追加ボタンを連打するなどのうっかりミスも安心、このボタンで`.civitai.info`ファイルに記録された元の名前に戻します。

## 実行方法

### 方法1: Pythonを扱えるひと向け。このリポジトリをクローンして、PyQt5をインストールして、`KRNS-renamer-alpha.py`を実行

以下のコマンドを１行ずつ実行してください。

```bash
pip install PyQt5
git clone https://github.com/kai-rin/KRNS.git
cd .\KRNS\
python KRNS-renamer-alpha.py
```

### 方法2: Windows環境でいちいちコマンドライン叩きたくないひと向け。 `KRNS-renamer-alpha.exe` をダウンロードして、ダブルクリックやエンターで実行

`KRNS-renamer-alpha.exe` はシンプルに `pyinstaller --onefile --noconsole --icon=KRNS-renamer-alpha.ico KRNS-renamer-alpha.py` で作成しただけのシンプルなものです。

## 仕組み

プログラムは各ディレクトリとサブディレクトリを処理して、`.civitai.info` ファイルを探します。このファイルに記述されている `modelId` や元のファイル名を使って、ファイル名を変更します

## コントリビューション

より良いアイデアあったりバグ見つけた人、めちゃくちゃ気軽にフォークして、ちょこっといじって、プルリクエスト送ってください。作者はソフトウェア開発能力いい加減なので、なんでもウェルカムだしたぶんめちゃくちゃ喜びます

## ライセンス

PyQt5のライセンスポリシーにのっとり GNU General Public License v3.0（GPLv3）で公開してます。

参考: <https://www.gnu.org/licenses/gpl-3.0.en.html>
