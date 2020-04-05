# Image Convolution

A convolution, in the sense of image processing, is a mathematical operation involving two matrices, where they are overlapped, multiplied and summed (the process is explained later and can be visualized in the image bellow).

Convolution may be used as filter applying technique and also as a feature extraction technique.

![Figure 1](https://icecreamlabs.com/wp-content/uploads/2018/08/33-con.gif)

## Definition

Given a image <img src="https://render.githubusercontent.com/render/math?math=I_{m \times n}"> (<img src="https://render.githubusercontent.com/render/math?math=m"> and <img src="https://render.githubusercontent.com/render/math?math=n"> are the height and width respectively) and a kernel <img src="https://render.githubusercontent.com/render/math?math=K_{h \times w}"> the convolution operation <img src="https://render.githubusercontent.com/render/math?math=I_{m \times n} * K_{h \times q}"> results in a third matrix <img src="https://render.githubusercontent.com/render/math?math=C"> defined by:

<center><img src="https://render.githubusercontent.com/render/math?math=C_{x, y} = \sum_{i=0}^{h} \sum_{j=0}^{w} I_{x'+i, y'+j} \times K{i, j},"></center>

where <img src="https://render.githubusercontent.com/render/math?math=x'=x - (h / 2)"> and <img src="https://render.githubusercontent.com/render/math?math=y'=y - (w / 2)">

## Algorithm

{TODO}

## References

[1] [Kernel (image processing)](https://en.wikipedia.org/wiki/Kernel_(image_processing)). Wikipedia.
[2] [Image Kernels](https://setosa.io/ev/image-kernels/). Victor Powell.
