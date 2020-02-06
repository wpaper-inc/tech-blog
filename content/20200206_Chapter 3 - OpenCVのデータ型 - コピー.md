Title: Learning OpenCV3のPython実装 (Chapter 3)
Date: 2020-02-06
Category: OpenCV3
Tags: 画像処理, OpenCV3, チュートリアル
Slug: learning-opencv3-chapter3
Authors: Kousuke Takeuchi
Summary: オライリーから出版されている「詳解 OpenCV3」を社内の新人レクチャーとして使用しています。こちらの本はC++でプログラムが提供されているため、pythonに翻訳したものをせっかくなので掲載しようと思い、本記事を書き出しました。
Header_Cover: images/20200203_learning-opencv3.jpeg
Og_Image: https://tech.wpaper-inc.com/images/20200203_learning-opencv3.jpeg
Twitter_Image: https://tech.wpaper-inc.com/images/20200203_learning-opencv3.jpeg

OpenCV3のデータ型 (Python版)

Pythonではcv::Matクラスの代わりにNumPyの配列クラスが使用されます


```python
import cv2

img = cv2.imread('img/lena.png')
type(img)
```




    numpy.ndarray



したがって、C++版のMatクラスやVecクラス、Pointクラスなどの代わりとなるPython向けの型を紹介します

### Pointクラス


```python
import numpy as np

point1 = np.array([1, 2]) # (x, y)
print(point1)
```

    [1 2]



```python
# アクセスはインデックスで指定、また内積や外積はNumPyの関数を使用する
print("x: {}, y: {}".format(point1[0], point1[1]))

point2 = np.array([2, 1])
print("inner prod: ", np.dot(point1, point2))
print("outer prod: ", np.outer(point1, point2))
```

    x: 1, y: 2
    inner prod:  4
    outer prod:  [[2 1]
     [4 2]]


スカラークラスやサイズクラスは、Pythonの数値型で代用できます

### Rect, RotatedRectクラス


```python
rect = ((10, 20), (30, 50)) # ((left_top.x, left_top.y), (right_bottom.x, (right_bottom.y)))
img = cv2.rectangle(img, rect[0], rect[1], (0, 255, 0), 3)
```

Matx, Vec, complexについても、同じくNumPyやPythonの数値/配列型を活用する

## ヘルパーオブジェクト

こちらもPythonでは提供されていません。(cv::TermCriteria, Range, Ptr<>, Exception, DataType, InputArray, OutputArray)

### ユーティリティ関数
こちらは、一部Python用に提供されているものがあります。
以下提供されていない関数
+ alignPtr()
+ alignSize()
+ allocate()
+ deallocate()
+ cvCeil()
+ CV_Assert()/DgbAssert()
+ CV_Error()
+ fastFree()
+ fastMalloc()
+ cvFloor()
+ format()
+ cvIsInf()
+ cvIsNaN()
+ cvRound()


```python
# アークタンジェント
cv2.fastAtan2(1, 1.7320508) # atan(y, x)
```




    29.997692108154297




```python
# 平方根
cv2.cubeRoot(2.0)
```




    1.2599210739135742




```python
# OpenCVのエラー型
cv2.error('some error')
```




    cv2.error('some error')




```python
# CPUのティック数を返す
cv2.getCPUTickCount()
```




    2543827866529




```python
# OpenCVに確保されたスレッドの総数
cv2.getNumThreads()
```




    13




```python
# OpenCVのcv:dft(離散フーリエ変換)に渡す配列のサイズ
cv2.getOptimalDFTSize(1000000000)
```




    1000000000




```python
# スレッドのID
cv2.getThreadNum()
```




    0




```python
# アーキテクチャ依存の時間に対する相対的なティックカウント
cv2.getTickCount()
```




    2546184901800




```python
# 単位時間の周波数
cv2.getTickFrequency()
```




    10000000.0




```python
# OpenCVが使えるスレッド数を設定する
cv2.setNumThreads(12)
cv2.getNumThreads()
```




    12




```python
# IPPなど外部ライブラリだけでなく、OpenCVにも最適化ライブラリがある
# この最適化を使うかどうか
cv2.setUseOptimized(True)
```


```python
# 最適化の設定を確認
cv2.useOptimized()
```




    True



### テンプレート構造
こちらもC++特有の言語仕様に合わせた機能なので、Pythonでの提供はありません

## 練習問題 (省略)
