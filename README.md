# PDF比較ツール
2つのPDFファイルを比較し，差分をハイライト表示するツールです．[出力例](./sample/new__old.pdf)

## 1. PDF比較ツールの起動方法
### 1.2 exeファイルから起動する方法


## 実行ファイルの作成方法
```sh
$ pip install pyinstaller
$ pyinstaller PDF_Comparator/main.py --name=PDF比較ツール --icon=img/icon.png --onefile --noconsole
```