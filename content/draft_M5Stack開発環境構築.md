Title: M5Stackシリーズ(1) - M5Stack開発環境構築
Date: 2020-01-08
Category: ESP32
Tags: エッジコンピューティング, M5Stack, ESP32
Slug: M5Stack-Series-1
Authors: Kousuke Takeuchi
Summary: M5Stack Grayを購入しました。本記事のシリーズでは、M5Stackの開発環境構築から、センサーを使った姿勢推定、そしてJeVoisでの顔検知と連携したサーボの制御まで解説していこうと思います。
Header_Cover: images/m5-header.jpg
Og_Image: images/m5-header.jpg
Twitter_Image: images/m5-header.jpg
Status: draft

### シリーズ

1. [(本記事) M5Stack開発環境構築](M5Stack-Series-1.html)
2. 6軸センサーデータの取得
3. 回転行列/クオータニオンの基礎
4. 静止状態でのカルマンフィルター/相補フィルターによるドリフト補正と姿勢推定
5. 動作状態でのドリフト補正と姿勢推定
6. 9軸センサーでの姿勢推定
7. サーボドライバーシールドとの連携
8. JeVoisの顔検知と追跡

[M5Stack Gray](https://www.switch-science.com/catalog/3648/)を購入しました。こちらには**MPU-9250 ９軸センサモジュール**が載っていて、通常3軸や6軸センサーでは3軸の角速度や角加速度を取得して初期位置からの移動を検出できます。また、別売りのシールドを搭載することで、サーボやモーターなどの外部デバイスの制御もArduinoと同様に簡単にできる端末となっています。本記事のシリーズでは、M5Stackの開発環境構築から、センサーを使った姿勢推定、そしてJeVoisでの顔検知と連携したサーボの制御まで解説していこうと思います。



https://strawberry-linux.com/pub/AK8963.pdf

https://www.fujiele.co.jp/semiconductor/ti/tecinfo/news201707140000/

http://watako-lab.com/2019/02/28/3axis_gyro/

https://lab.fujiele.co.jp/articles/3962/

https://strawberry-linux.com/catalog/items?code=12250