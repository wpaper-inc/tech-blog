Title: JeVois Tutorial(3) Tesseractを使ったテキスト画像処理(OCR)
Date: 2020-02-04
Category: AI, 画像処理
Tags: エッジコンピューティング, 画像処理, JeVois
Slug: JeVois-Tutorial-3
Authors: Kousuke Takeuchi
Summary: JeVois上で、Googleが提供するTesseractを使ったOCR処理を実行します。
Header_Cover: images/20200106_jevois-header.jpg
Og_Image: images/20200106_JeVois_tg2e9bgo.jpg
Twitter_Image: images/20200106_JeVois_tg2e9bgo.jpg

手書き文字の認識にはMNISTを用いたディープラーニングが入門編としてよく紹介されていますが、業務レベルで使用できる有名な紙の書類の文字認識として、Googleがオープンソースで提供している「[Tesseract(テッセラクト)](https://tesseract-ocr.github.io/)」があります。

Tesseractが素晴らしい理由として、日本語のOCRにも対応している上に、OpenCVでもモジュールとして使用できる点があります。

今回は[こちらの記事](http://jevois.org/tutorials/ProgrammerInvOCR.html)を参考に、TesseractをJeVois上で実行する方法について紹介します。

## 1. Pythonの新規モジュールプロジェクトを作成

TesseractはPythonで提供されているため、これまで紹介したC++のプロジェクトとは実装言語が異なります。しかし環境の構築方法や開発・デバイスでの実機動作についてはほぼ同じプロセスで行うことができます。

・環境構築については、[こちら](20200106_Ubuntu18.04でJeVois開発環境作成と、サンプルコードをコマンドラインから実行)を参考にしてください

新規モジュールを作成するには、C++の場合は`jevois-create-module`コマンドを使用しましたが、Pythonの場合は`jevois-create-python-module`を使用します

```shell
$ jevois-create-python-module Whitepaper TesseractOCR
```

すると、C++の場合と同様にモジュールのフォルダが作成されます。一点C++の場合と相違があるのは、`src`以下のディレクトリに`.C`ファイルではなく`.py`ファイルが作成されることです。

```shell
$ tree ./tesseractocr

tesseractocr
├── CMakeLists.txt
├── COPYING
├── INSTALL
├── README.md
├── rebuild-host.sh
├── rebuild-platform.sh
├── share
│   └── README.txt
└── src
    └── Modules
        └── TesseractOCR
            ├── TesseractOCR.py
            └── postinstall
```

## 2. TesseractOCRを使ったPython実装

続いて、`src/Modules/TesseractOCR/TesseractOCR.py`を編集します。

```python
import libjevois as jevois
import cv2
import numpy as np

class TesseractOCR:
    def __init__(self):
        # Tesseractの初期化
        self.ocr = cv2.text.OCRTesseract_create()
        
    def process(self, inframe, outframe):
        img = inframe.getCvBGR()
        # 画像をTesseractに渡して、認識した文字を返す
        txt = cv2.text_OCRTesseract.run(self.ocr, img, 50)
        # 認識した文字を画像に表示
        msgbox = np.zeros((60, img.shape[1], 3), dtype = np.uint8) + 80
        cv2.putText(msgbox, txt, (3, 40), cv2.FONT_HERSHEY_SIMPLEX,
          0.8, (255,255,255), 2, cv2.LINE_AA)
        out = np.vstack((img, msgbox))
        # 画像をシリアル経由で返す
        outframe.sendCv(out)
```

C++の場合と比べて、Pythonは非常にシンプルにかけます。`process`関数に引数として入力フレームと出力フレームが渡されるので、

1. 入力フレームから画像を取得
2. 画像をTesseractで解析し、OpenCVで画像操作する
3. 操作した画像を出力フレームに渡す

といった感じで処理してあげればOKです。process関数内で処理してあげることに注意すれば、通常のPythonを使ったOpenCVのプロジェクトとほとんど相違なく実装を進めることができます。

## 3. ホストでの実行

続いてPythonのプログラムをホストマシンで実行します。まずはプロジェクトをホストビルドします

```shell
$ ./rebuild-host.sh 
```

次に、ビデオマッピングの設定ファイルに、TesseractOCRを追加します。

```shell
$ echo "YUYV 320 300 30 YUYV 320 240 30 Whitepaper TesseractOCR" | sudo tee -a /jevois/config/videomappings.cfg
```

カメラデバイスが接続されていることを確認し、

```shell
$ v4l2-ctl --list-devices
USB_Camera: USB_Camera (usb-0000:00:0c.0-2):
        /dev/video0
        /dev/video1
```

さらに`jevois-daemon`でビデオマッピングのIDを調べます

```shell
$ jevois-daemon
> listmappings
   ...
   37 - OUT: YUYV 320x308 @ 30fps CAM: YUYV 320x240 @ 30fps MOD: JeVois:TensorFlowEasy C++
   38 - OUT: YUYV 320x300 @ 30fps CAM: YUYV 320x240 @ 30fps MOD: Whitepaper:TesseractOCR Python
   39 - OUT: YUYV 320x290 @ 60fps CAM: YUYV 320x240 @ 60fps MOD: JeVois:FirstVision C++
   ...
> quit
```

こちらの環境では、38番に割り振られていたため、このIDとデバイスパスを指定して、再度jevois-daemonを起動します。

```shell
$ jevois-daemon --videomapping=38 --cameradev=/dev/video0
```

実行した結果がこちら

![20200204_tesseractocr-host.png]()

バチッと認識してくれるわけではなさそうですが、それなりに文字おこしが出来ていることが確認出来ました。

## 4. JeVoisデバイスでTesseractOCRを実行

jevois-daemonを一旦止めて、最後にJeVoisにモジュールを書き込んで、JeVois上でOCRを実行してみましょう。

```shell
$ jevois-usbsd start
$ ./rebuild-platform --live
```

guvcviewでJeVoisから送られてくる処理済みの画像を確認します

```shell
$ guvcview -d /dev/video2
```

ホストマシンと同様に、OCR処理された画像を確認することができました。