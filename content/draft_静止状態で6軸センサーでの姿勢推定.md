Title: M5Stackシリーズ(4) - 姿勢の補正
Date: 2020-01-08
Category: ESP32
Tags: エッジコンピューティング, M5Stack, ESP32
Slug: M5Stack-Series-4
Authors: Kousuke Takeuchi
Summary: M5Stack Grayを購入しました。本記事のシリーズでは、M5Stackの開発環境構築から、センサーを使った姿勢推定、そしてJeVoisでの顔検知と連携したサーボの制御まで解説していこうと思います。
Header_Cover: images/m5-header.jpg
Og_Image: images/m5-header.jpg
Twitter_Image: images/m5-header.jpg
Status: draft

[ジャイロのドリフト補正と比較（カルマン、相補フィルター）](https://garchiving.com/gyro-drift-correction/)

6軸センサーにはジャイロセンサーが搭載されていますが、ノイズや温度変化によって誤差が生じてしまいます(ドリフト現象)。ドリフトの誤差が蓄積されることで、停止状態でも角度が少しずつ計算上ずれます。

ここで、ジャイロセンサーから取得できる角速度を$\dot\theta(t) = \frac{d\theta(t)}{dt} [rad/s]$、センサーのローカル座標系における回転角度を$\theta(t)[rad]$とすると、微小時間における角の変動が角速度なので、$T$[s]の間で角速度を取得すれば
$$
\theta = \oint d\theta(t) = \int_0^T \frac{d\theta(t)}{dt}dt = \int_0^T \dot\theta(t) dt \approx \sum_{t=0}^T \dot\theta(t)
$$
つまり、ジャイロセンサーを単純に足し合わせるだけで現在の角度を取得することが出来ます。

しかしジャイロセンサーにはドリフトが発生して誤差が蓄積されるため、6軸センサーに搭載されている角加速度センサーを使って、同様に角度を算出します。角加速度は$\dot\theta[rad/s^2]$とします。
$$
\dot\theta(t) = \int_0^T \ddot\theta(t)dt \\\theta = \int_0^T\dot\theta(t)dt = \iint_t\ddot\theta(t)
$$
これで角速度センサーと角加速度センサーからの2通りで角度を計算できました。どちらも理論上は同じ値になりますが、ただ現実のセンサーでは、角速度センサーが低周波、角加速度センサーが高周波のデータをとれるなど、それぞれのセンサーに特性があって、誤差の受け方も様々です。そこで、両者のセンサーデータから互いに補正しあって、精密な値を推定しようというのがカルマンフィルターになります。