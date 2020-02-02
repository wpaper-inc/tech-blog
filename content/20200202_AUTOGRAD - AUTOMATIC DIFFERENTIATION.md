Title: PyTorch Tutorial翻訳 - Autograd
Date: 2020-02-02
Category: ESP32
Tags: ディープラーニング, AI, PyTorch, チュートリアル
Slug: pytorch-autograd
Authors: Kousuke Takeuchi
Summary: PyTorch Tutorialの日本語訳です。最近TensorFlowからPyTorchに切り替えた際に学習で使用した公式サイトですが、日本語訳が見つからなかったので訳文を作成しました。今回はDEEP LEARNING WITH PYTORCH: A 60 MINUTE BLITZのAutograd : Automatic Differentiationについての日本語訳になります。Header_Cover: images/20200202_autodiff.png
Og_Image: https://tech.wpaper-inc.com/images/20200202_autodiff.png
Twitter_Image: https://tech.wpaper-inc.com/images/20200202_autodiff.png

[PyTorch Tutorial](https://pytorch.org/tutorials/)の日本語訳です。最近TensorFlowからPyTorchに切り替えた際に学習で使用した公式サイトですが、日本語訳が見つからなかったので訳文を作成しました。



今回は[DEEP LEARNING WITH PYTORCH: A 60 MINUTE BLITZ](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)の[Autograd : Automatic Differentiation](https://pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html#sphx-glr-beginner-blitz-autograd-tutorial-py)についての日本語訳になります。



Auto Grad : 自動微分
PyTorchにおけるニューラルネットワークの主題は`autograd`パッケージである。簡単に体験して、初めてのニューラルネットを試してみる。

`autograd`パッケージはすべてのテンソルでの演算における自動微分を提供する。「define-by-run」のフレームワークであり、つまりコードがどのように実行されるかによってバックプロパゲーションが定義され、各イテレーションは別とできる。

## Tensor

`torch.Tensor`はパッケージでも中心的なクラスである、`.requires_grad`がTrueになっていれば、すべての演算を追跡し始めて、計算が終了した段階で`.backward()`を呼び出せるようになる。そして自動的にすべての勾配が計算される。計算された勾配はテンソルに`.grad`属性として蓄積される。

テンソルを追跡履歴からやめる場合は、`.detach()`を呼び出して計算履歴から取り除き、今後の計算では追跡されないようにする。

追跡履歴に入れたくない場合は、コードブロックを`with torch.no_grad():`フレーズで囲ってあげる。これはモデルを評価する場合に部分的に有効となりうる。なぜならモデルは`requires_grad=True`の際にパラメータがトレーニングされうるものとなり、評価の際には勾配は不要であるからである。

自動微分を実装する際に重要なクラスがもう一つある。それは`Function`である。

`Tensor`と`Function`は内部接続されており、かつ非周期的なグラフを構築する。そのグラフは計算履歴をエンコードしたもの。それぞれのテンソルは`.grad_fn`属性を持っており、これは`Tensor`によって作成された`Function`クラスである。

もしデリバティブを計算したい場合は、テンソルの`.backward()`を実行する。テンソルがスカラー型の場合は、`.backward()`を実行する必要はないが、もし要素がより存在する場合には、テンソルの形があっているかを示す`gradient`属性を指定する必要がある。


```python
import torch
```

計算を追跡するために、`required_grad=True`となるテンソルを作成


```python
x = torch.ones(2, 2, requires_grad=True)
print(x)
```

    tensor([[1., 1.],
            [1., 1.]], requires_grad=True)


テンソルの演算を実行


```python
y = x + 2
print(y)
```

    tensor([[3., 3.],
            [3., 3.]], grad_fn=<AddBackward0>)


yは演算結果なので、`grad_fn`を持つ


```python
print(y.grad_fn)
```

    <AddBackward0 object at 0x000001DB25EA2128>


yについてさらに演算を実行


```python
z = y * y * 3
out = z.mean()

print(z, out)
```

    tensor([[27., 27.],
            [27., 27.]], grad_fn=<MulBackward0>) tensor(27., grad_fn=<MeanBackward0>)


`.required_grad_()`で作成済みのテンソルの`requires_grad`フラグを変更する。何も与えていなければ`False`になる


```python
a = torch.randn(2,2)
a = ((a * 3) / (a - 1))
print(a.requires_grad)
```

    False



```python
a.requires_grad_(True)
print(a.requires_grad)
```

    True



```python
b =(a * a).sum()
print(b.grad_fn)
```

    <SumBackward0 object at 0x000001DB25EAF208>


## 勾配
バックプロパゲーションについてトライしてみる。`out`は1要素のスカラーをもつので、`out.backward(torch.tensor(1.)`と同じになる


```python
out.backward()
```


```python
print(x.grad)
```

    tensor([[4.5000, 4.5000],
            [4.5000, 4.5000]])

4.5を要素に持つ行列が出力された、`out`テンソルを"$o$"とする。 $o = \frac{1}{4}\sum_i z_i, z_i = 3(x_i + 2)^2$で、$\left.z_i\right|_{x_i=1} = 27$。したがって、$\frac{\partial{o}}{\partial{x_i}} = \frac{3}{2}(x_i+2)$より、$\left.\frac{\partial{o}}{\partial{x_i}}\right|_{x_i=1} = \frac{9}{2} = 1$


数学的には、ベクトル関数$\vec{y} = f(\vec{{x}})$が与えられたとき、$\vec{y}$の勾配はヤコブ行列を用いて、以下で定義される
$$
J = \left(
    \begin{array}{ccc}
      \frac{\partial{y_1}}{\partial{x_1}} & \ldots & \frac{\partial{y_1}}{\partial{x_n}} \\
      \vdots & \ddots & \ldots \\
      \frac{\partial{y_n}}{\partial{x_1}} & \ldots & \frac{\partial{y_n}}{\partial{x_n}}
    \end{array}
  \right)
$$

一般的に、`torch.autograd`はベクトルとヤコビアンの掛け算のためのエンジンである、つまり、ベクトルが$v = (v_1, v_2, \ldots, v_m)^T$で与えられたとき、行列積$v^\mathrm{T} \cdot J$で計算される。もし$v$がスカラーの関数$l = g(\vec{v})$で計算された場合、$(l \in \mathbb{R}^1)$、$v = \left(\frac{\partial{l}}{\partial{y_1}} \cdots \frac{\partial{l}}{\partial{y_m}}\right)$で、結合則からベクトルとヤコビアンの行列積は $\vec{x}$からみた$l$の勾配となる

$$
J^\mathrm{T} \cdot v =
\left(
    \begin{array}{ccc}
      \frac{\partial{y_1}}{\partial{x_1}} & \ldots & \frac{\partial{y_1}}{\partial{x_n}} \\
      \vdots & \ddots & \ldots \\
      \frac{\partial{y_m}}{\partial{x_1}} & \ldots & \frac{\partial{y_m}}{\partial{x_n}}
    \end{array}
  \right) \left(
    \begin{array}{c}
      \frac{\partial{l}}{\partial{y_1}} \\
      \vdots \\
      \frac{\partial{l}}{\partial{y_m}}
    \end{array}
  \right)
  = \left(
    \begin{array}{c}
      \frac{\partial{l}}{\partial{x_1}} \\
      \vdots \\
      \frac{\partial{l}}{\partial{x_m}}
    \end{array}
  \right)
$$

ベクトルとヤコビアンの行列積について、例を見てみる


```python
x = torch.randn(3, requires_grad=True)

y = x * 2
while y.data.norm() < 1000:
    y = y * 2

print(y)
```

    tensor([ -225.5253, -1781.9635,  -195.9621], grad_fn=<MulBackward0>)


この場合、yはスカラーではない。`torch.autograd`はヤコビアンを直接計算することはできない。しかし、ベクトルとヤコビアンの積が欲しいとき、`backward`にベクトルを引数として実行すればよい


```python
v = torch.tensor([0.1, 1.0, 0.00010], dtype=torch.float)
y.backward(v)

print(x.grad)
```

    tensor([1.0240e+02, 1.0240e+03, 1.0240e-01])


`.requires_grad=True`による自動微分を停止する場合、コードブロックを`with torch.no_grad()`で囲ってあげる


```python
print(x.requires_grad)
print((x ** 2).requires_grad)
```

    True
    True



```python
with torch.no_grad():
    print((x ** 2).requires_grad)
```

    False


もしくは、`.detach()`を使う


```python
print(x.requires_grad)
y = x.detach()
print(y.requires_grad)
print(x.eq(y).all())
```

    True
    False
    tensor(True)


`autograd.Function`については[こちらのドキュメント](https://pytorch.org/docs/stable/autograd.html#function)を参照
