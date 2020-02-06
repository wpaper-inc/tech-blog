Title: Learning OpenCV3のPython実装 (Chapter 2)
Date: 2020-02-03
Category: OpenCV3
Tags: 画像処理, OpenCV3, チュートリアル
Slug: learning-opencv3-chapter2
Authors: Kousuke Takeuchi
Summary: 今回はDEEP LEARNING WITH PYTORCH- A 60 MINUTE BLITZのAutograd - Automatic Differentiationについての日本語訳になります。
Header_Cover: images/20200203_learning-opencv3.jpeg
Og_Image: https://tech.wpaper-inc.com/images/20200203_learning-opencv3.jpeg
Twitter_Image: https://tech.wpaper-inc.com/images/20200203_learning-opencv3.jpeg



オライリーから出版されている「[詳解 OpenCV3](https://www.oreilly.co.jp/books/9784873118376/)」を社内の新人レクチャーとして使用しています。こちらの本はC++でプログラムが提供されているため、pythonに翻訳したものをせっかくなので掲載しようと思い、本記事を書き出しました。

インクルードファイルについては、PythonのOpenCVライブラリではcv2モジュールに統一されているため、ここでは省きます
(C++で利用する場合、oepncv.hppをインクルードすることで、あらゆる関数を利用できるようになります)

### 写真を表示
C++ HighGUIのツールキットの一部を使用します (opencv2/highgui/highgui.hpp)


```python
import cv2

def main(image_file):
    # ファイル名に基づいて、読み込むファイルのフォーマットを決定する(BMP,DIB,JPEG,PNGなど)
    img = cv2.imread(image_file)
    # C++と違い、Python版はNumPyの配列クラスを返す
    if img is None:
        return
    # 画像の保持と表示が可能なウィンドウ画面を表示
    # 第2引数にはウィンドウのプロパティを指定 (default: WINDOW_AUTOSIZE)
    cv2.namedWindow("Example 2-1", cv2.WINDOW_AUTOSIZE)
    # namedWindowsで作成されたウィンドウに画像を表示
    cv2.imshow("Example 2-1", img)
    # キー入力がくるまで待つ. 正の数が引数に与えられた場合は、その数のミリ秒だけ待機
    cv2.waitKey(0)
    # ウィンドウを破棄
    cv2.destroyWindow("Example 2-1")

image_file = "./img/lena.png"
main(image_file)
```

### 動画
カメラからフレームを読み込んで、カメラ画像を再生します


```python
import cv2

# デバイス番号, デバイスファイルのパスを指定してもOK
device_number = 0

cv2.namedWindow("Example 2-3")
cap = cv2.VideoCapture(device_number)

while True:
    # VideoCaptureオブジェクトのデータストリームからフレームごとに読み込まれる
    ret, frame = cap.read()
    # 何も読み込まれなかったら、retがFalseになる
    if not ret:
        break
    cv2.imshow("Example 2-3", frame)
    # フレームを表示した後、何かキーが押されるまで33ミリ秒待つ
    if cv2.waitKey(33) >= 0:
        break

# 本には載っていなかったが、ウィンドウを破棄する必要がある
cv2.destroyWindow("Example 2-3")
# さらにデータストリームも破棄する必要がある
cap.release()
```

### 動き回る
プログラムを拡張し、動画の中を自由に動き回れるようにします。上記のプログラムでは、フレームが順番に流れて表示されるだけです。
そこで次は、トラックバーを用いたスライダーをつけて動き回れるようにします。さらにSキーを押すことで動画をコマ送り、Rキーで通常の再生モードに戻れるようにします

HiGUIツールキットは、表示関数以外にもトラックバーの機能も提供しています。(cv2.createTrackbar())


```python
import cv2

video_file = "video/vtest.avi"

g_slider_position = 0 # トラックバーのスライダー位置を保持する
g_run = 1 # ステップ再生モードで始める (負の数は連続モードで再生していることを表す, 0の場合は停止)
g_dontset = 0 # ステップ再生モードに切り替わる前にトラックバーの位置を更新

g_cap = cv2.VideoCapture(video_file)

# トラックバーの位置を更新
def on_trackbar_slide(pos):
    global g_cap, g_dontset, g_run
    # フレームの位置を更新
    g_cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
    
    if not g_dontset:
        g_run = 1
    g_dontset = 0

cv2.namedWindow("Example 2-4", cv2.WINDOW_AUTOSIZE)
# 合計フレーム数、フレームの幅と高さを取得
frames = int(g_cap.get(cv2.CAP_PROP_FRAME_COUNT))
tmpw = g_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
tmph = g_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("Video has {} frames of dimensions({}, {})".format(frames, tmpw, tmph))

# createTrackbar(バーのラベル, 表示するウィンドウ名, 最小値, 最大値, コールバック関数)
cv2.createTrackbar("Position", "Example 2-4", g_slider_position, frames, on_trackbar_slide)

while True:
    # g_run = 1の場合はステップ再生、g_run < 0の場合は常時再生
    if g_run != 0:
        ret, frame = g_cap.read()
        if not ret:
            break
        # 現在のフレーム位置を取得
        current_pos = int(g_cap.get(cv2.CAP_PROP_POS_FRAMES))
        g_dontset = 1
        
        cv2.setTrackbarPos("Position", "Example 2-4", current_pos)
        cv2.imshow("Example 2-4", frame)
        
        g_run -= 1
    
    c = cv2.waitKey(10)
    if c < 0:
        continue
    c = chr(c)
    print(c)
    if c == 's': # ステップ再生モード
        g_run = 1
        print("Single step, run = {}".format(g_run))
    if c == 'r':
        g_run = -1
        print("Run mode, run = {}".format(g_run))
    if c == 27:
        break

# 本には載っていなかったが、ウィンドウを破棄する必要がある
cv2.destroyWindow("Example 2-4")
# さらにデータストリームも破棄する必要がある
g_cap.release()
```

### 簡単な変換

コンピュータビジョンについて試してみましょう。動画のストリームに対してフィルタを適用します。

一番簡単な処理は、画像の平滑化です。Gaussian(ガウシアン)やカーネル関数で畳み込み処理をすることで、画像の情報量を効率的に減らします。


```python
import cv2

image = cv2.imread("./img/lena.png")

# 入力画像と出力画像を表示するウィンドウを作成する
cv2.namedWindow("Example 2-5-in", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("Example 2-5-out", cv2.WINDOW_AUTOSIZE)

# 入力画像をウィンドウに表示
cv2.imshow("Example 2-5-in", image)

# 平滑化処理をする
# ガウシアンカーネルのサイズは5x5に設定
out = cv2.GaussianBlur(image, (5,5), 3, 3)
# 2回処理する
out = cv2.GaussianBlur(out, (5,5), 3, 3)

# 平滑化した画像を出力ウィンドウに表示する
cv2.imshow("Example 2-5-out", out)

cv2.waitKey(0)

cv2.destroyWindow("Example 2-5-in")
cv2.destroyWindow("Example 2-5-out")
```

![out](./out/example-2-5-out.png)

### 少し複雑な変換




```python
import cv2

cv2.namedWindow("Example 2-6-in", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("Example 2-6-out", cv2.WINDOW_AUTOSIZE)

img1 = cv2.imread("./img/lena.png")
cv2.imshow("Example 2-6-in", img1)

# ガウシアンフィルターとダウンサンプリング (画像サイズを1/2にする)
img2 = cv2.pyrDown(img1)
cv2.imshow("Example 2-6-out", img2)

cv2.waitKey(0)

cv2.destroyWindow("Example 2-6-in")
cv2.destroyWindow("Example 2-6-out")
```

### AVIファイルへ書き込む
cv2.VideoWriterを使って、入力フレームを一つずつ書き込む装置を作成することができます。


```python
import cv2

video_file = "video/vtest.avi"
out_file = "out/log_polar.avi"

cv2.namedWindow("Example 2-11", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("Log_Polar", cv2.WINDOW_AUTOSIZE)

capture = cv2.VideoCapture(video_file) # カメラID=0を与えれば、カメラからキャプチャ

fps = int(capture.get(cv2.CAP_PROP_FPS))
size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

writer = cv2.VideoWriter(out_file, cv2.VideoWriter_fourcc('M','J','P','G'), fps, size)

while True:
    ret, bgr_frame = capture.read()
    if not ret:
        break
    
    cv2.imshow("Example 2-11", bgr_frame)
    
    # 出力(対数極座標フレーム)
    logpolar_frame = cv2.logPolar(
        bgr_frame,             # 入力 (カラーフレーム)
        bgr_frame.shape[:2],   # [width, height, : channel]
        40,                   # 大きさ (スケールパラメータ)
        cv2.WARP_FILL_OUTLIERS  # 外れ値を「0」で塗りつぶす
    )
    
    cv2.imshow("Log_Polar", logpolar_frame)
    writer.write(logpolar_frame)
    
    c = cv2.waitKey(33)
    if c == ord('q'):
        break
    
capture.release()
writer.release()
cv2.destroyWindow("Example 2-11")
cv2.destroyWindow("Log_Polar")
```

## 練習問題

### 1. 略
### 2.
C++のサンプルで提供されているlkdemoはPythonで実装されていないため、代わりにpythonディレクトリにあるlk_homographyを実行する


```python
!cd sample & python lk_homography.py
```

### 3.


```python
import cv2

video_file = "video/vtest.avi"
out_file = "out/down_sample.avi"

cv2.namedWindow("Exercise 2-3", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("DownSampled", cv2.WINDOW_AUTOSIZE)

capture = cv2.VideoCapture(video_file) # カメラID=0を与えれば、カメラからキャプチャ

fps = int(capture.get(cv2.CAP_PROP_FPS))
size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

writer = cv2.VideoWriter(out_file, cv2.VideoWriter_fourcc('M','J','P','G'), fps, size)

while True:
    ret, bgr_frame = capture.read()
    if not ret:
        break
    
    cv2.imshow("Exercise 2-3", bgr_frame)
    
    # 出力(ダウンサンプリング)
    down_frame = cv2.pyrDown(bgr_frame)
    
    cv2.imshow("DownSampled", down_frame)
    writer.write(down_frame)
    
    c = cv2.waitKey(33)
    if c == ord('q'):
        break
    
capture.release()
writer.release()
cv2.destroyWindow("Exercise 2-3")
cv2.destroyWindow("DownSampled")
```

### 4.


```python
import cv2

video_file = "video/vtest.avi"

pos = 0

g_cap = cv2.VideoCapture(video_file)

# オートリサイズされると小さい画像の時にトラックバーが隠れるので、
# cv2.AUTOSIZEではなくWINDOW_NORMALを指定
# 画面の幅が小さいときはマウスで直接大きさを変更する
cv2.namedWindow("Exercise 2-4", cv2.WINDOW_NORMAL)
size = (int(g_cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(g_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# createTrackbar(バーのラベル, 表示するウィンドウ名, 最小値, 最大値, コールバック関数)
cv2.createTrackbar("Position", "Exercise 2-4", 0, 3, lambda pos: None)

while True:
    ret, frame = g_cap.read()
    if not ret:
        break
    
    # 0 -> 1/1, 1 -> 1/2, 2 -> 1/4, 3 -> 1/8の縮小サイズで定義
    # つまり、1/縮小サイズ = 2**pos
    pos = cv2.getTrackbarPos("Position", "Exercise 2-4")
#     scale = 2**pos
#     dstsize = (size[0]//scale, size[1]//scale)
#     if scale > 1:
#         down_frame = cv2.pyrDown(frame, dstsize=dstsize)
    down_frame = frame
    for _ in range(pos):
        down_frame = cv2.pyrDown(down_frame)
    cv2.imshow("Exercise 2-4", down_frame)

    c = cv2.waitKey(10)
    if c == ord('q'):
        break

# 本には載っていなかったが、ウィンドウを破棄する必要がある
cv2.destroyWindow("Exercise 2-4")
# さらにデータストリームも破棄する必要がある
g_cap.release()
```
