Title: PyTorch Tutorial翻訳 - What is PyTorch
Date: 2020-01-31
Category: ESP32
Tags: ディープラーニング, AI, PyTorch, チュートリアル
Slug: pytorch-tutorial-what-is-pytorch
Authors: Kousuke Takeuchi
Summary: 今回はDEEP LEARNING WITH PYTORCH - A 60 MINUTE BLITZのWhat is PyTorchについての日本語訳になります。
Header_Cover: images/20200131_tensor_illustration_flat.png
Og_Image: https://tech.wpaper-inc.com/images/20200131_tensor_illustration_flat.png
Twitter_Image: https://tech.wpaper-inc.com/images/20200131_tensor_illustration_flat.png

[PyTorch Tutorial](https://pytorch.org/tutorials/)の日本語訳です。最近TensorFlowからPyTorchに切り替えた際に学習で使用した公式サイトですが、日本語訳が見つからなかったので訳文を作成しました。



今回は[DEEP LEARNING WITH PYTORCH: A 60 MINUTE BLITZ](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)の[What is PyTorch](https://pytorch.org/tutorials/beginner/blitz/tensor_tutorial.html#sphx-glr-beginner-blitz-tensor-tutorial-py)についての日本語訳になります。



## Getting Started

Tensor(テンソル)はNumPyのndarrayに似ています。加えてGPUを使って計算を高速化することもできます


```python
import torch
```

5x3の行列を作成します(初期化されていません)


```python
x = torch.empty(5,3)
print(x)
```

    tensor([[-2.7076e-05,  6.2778e-43, -2.7076e-05],
            [ 6.2778e-43, -2.7081e-05,  6.2778e-43],
            [-2.7081e-05,  6.2778e-43, -2.7081e-05],
            [ 6.2778e-43, -2.7081e-05,  6.2778e-43],
            [-2.7076e-05,  6.2778e-43, -2.7076e-05]])


ランダムに初期化した行列を作成


```python
x = torch.rand(5,3)
print(x)
```

    tensor([[0.5394, 0.3322, 0.3141],
            [0.0160, 0.1287, 0.2619],
            [0.6140, 0.8952, 0.2228],
            [0.9173, 0.4548, 0.4449],
            [0.8071, 0.7337, 0.6926]])


long型の0で埋めた行列


```python
x = torch.zeros(5,3, dtype=torch.long)
print(x)
```

    tensor([[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]])


データから直接テンソルを作成


```python
x = torch.tensor([5.5, 3])
print(x)
```

    tensor([5.5000, 3.0000])


もしくはすでに作成済みのテンソルをベースに新しいテンソルを作成します。この方法は入力されるテンソルの属性を再利用します。例えば新しい値をユーザーから与えられない場合はdtypeを再利用します


```python
x = x.new_ones(5,3,dtype=torch.double) # "new_*" メソッドはサイズを引数とします
print(x)
```

    tensor([[1., 1., 1.],
            [1., 1., 1.],
            [1., 1., 1.],
            [1., 1., 1.],
            [1., 1., 1.]], dtype=torch.float64)



```python
x = torch.rand_like(x, dtype=torch.float) # dtypeをオーバーライド
print(x) # 同じサイズのテンソルが結果として出力
```

    tensor([[0.1421, 0.9320, 0.3284],
            [0.5061, 0.6266, 0.2625],
            [0.1389, 0.6822, 0.6933],
            [0.0986, 0.3421, 0.9948],
            [0.2789, 0.5966, 0.5099]])


テンソルのサイズを取得


```python
print(x.size()) # 実際にはタプルと同じです。タプルの演算もサポートしています
```

    torch.Size([5, 3])


## Operations

演算を行うには、いくつか方法があります。次の例では、足し算の演算をします


```python
# 加算 - 文法1
y = torch.rand(5,3)
print(x + y)
```

    tensor([[0.6393, 1.7859, 0.7282],
            [0.8924, 1.2680, 0.9345],
            [0.7043, 1.6796, 1.1564],
            [0.8038, 0.6314, 1.3736],
            [0.9821, 0.6839, 0.6820]])



```python
# 加算 - 文法2
print(torch.add(x, y))
```

    tensor([[0.6393, 1.7859, 0.7282],
            [0.8924, 1.2680, 0.9345],
            [0.7043, 1.6796, 1.1564],
            [0.8038, 0.6314, 1.3736],
            [0.9821, 0.6839, 0.6820]])


追加: 出力用テンソルを引数に取る場合


```python
result = torch.empty(5,3)
torch.add(x, y, out=result)
print(result)
```

    tensor([[0.6393, 1.7859, 0.7282],
            [0.8924, 1.2680, 0.9345],
            [0.7043, 1.6796, 1.1564],
            [0.8038, 0.6314, 1.3736],
            [0.9821, 0.6839, 0.6820]])


追加: 破壊的メソッド


```python
# xをyに足す
y.add_(x)
print(y)
```

    tensor([[0.6393, 1.7859, 0.7282],
            [0.8924, 1.2680, 0.9345],
            [0.7043, 1.6796, 1.1564],
            [0.8038, 0.6314, 1.3736],
            [0.9821, 0.6839, 0.6820]])


NumPyと同様に、新しい機能が追加されたインデックスアクセスができます


```python
print(x[:, 1])
```

    tensor([0.9320, 0.6266, 0.6822, 0.3421, 0.5966])


サイズ変更: もしサイズを変える場合は、`torvch.view`を使えます


```python
x = torch.randn(4, 4)
y = x.view(16)
z = x.view(-1, 8)
print(x.size(), y.size(), z.size())
```

    torch.Size([4, 4]) torch.Size([16]) torch.Size([2, 8])


もしテンソルが1つだけ要素を持っている場合は、`.item()`を使うとPython数値型の値を取り出せます


```python
x = torch.randn(1)
print(x)
print(x.item())
```

    tensor([0.5599])
    0.5599286556243896


100個以上の演算について、[こちら](https://pytorch.org/docs/stable/torch.html)で解説しています

## NumPy Bridge

テンソルをNumPyの配列に変換します

TorchのテンソルとNumPy配列は、メモリの格納場所を共有しており、一方を変更するともう一方も変更されます

### TorchのテンソルをNumPy配列に変換


```python
a = torch.ones(5)
print(a)
```

    tensor([1., 1., 1., 1., 1.])



```python
b = a.numpy()
print(b)
```

    [1. 1. 1. 1. 1.]



```python
a.add_(1)
print(a)
print(b)
```

    tensor([2., 2., 2., 2., 2.])
    [2. 2. 2. 2. 2.]


### NumPy配列をTorchテンソルに変換


```python
import numpy as np
a = np.ones(5)
b = torch.from_numpy(a)
np.add(a, 1, out=a)
print(a)
print(b)
```

    [2. 2. 2. 2. 2.]
    tensor([2., 2., 2., 2., 2.], dtype=torch.float64)


CPU上のテンソルは、CharTensor(文字テンソル)を除いてNumPyへの変換をサポートしています

## CUDA Tensor

テンソルは、`.to`メソッドで他のデバイスに移動することが出来ます


```python
if torch.cuda.is_available():
    device = torch.device("cuda") # CUDAデバイスオブジェクト
    y = torch.ones_like(x, device=device) # GPUに直接テンソルを作成
    x = x.to(device) # もしくは、''.to("cuda")''を呼び出しても同じ
    z = x + y
    print(z)
    print(z.to("cpu", torch.double)) # ''.to''はdtypeを変更することもできる
```
