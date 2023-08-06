# QNQ -- QNQ's not quantization

## Description

The toolkit is for Techart algorithm team to quantize their custom neural network's pretrained model.
The toolkit is beta now, you can contact me with email(dongzhiwei2021@outlook.com) for adding ops and fixing bugs.

## How to install

`pip install qnq`

## How to quantize

1. Prepare your model.
   1. Check if your model contains non-class operator, like torch.matmul.
   2. If `True`, add `from qnq.operators.torchfunc_ops import *` to your code.
   3. Then use class replace non-class operator, you can refer fellow `#! add by dongz`

    ```python

    class BasicBlock(nn.Module):
        expansion = 1

        def __init__(self, inplanes, planes, stride=1, downsample=None):
            super(BasicBlock, self).__init__()
            self.conv1 = conv3x3(inplanes, planes, stride)
            self.bn1 = nn.BatchNorm2d(planes)
            self.relu1 = nn.ReLU(inplace=True)
            self.relu2 = nn.ReLU(inplace=True)
            self.conv2 = conv3x3(planes, planes)
            self.bn2 = nn.BatchNorm2d(planes)
            self.downsample = downsample
            self.stride = stride

            #! add by dongz
            self.torch_add = TorchAdd()

        def forward(self, x):
            identity = x

            out = self.conv1(x)
            out = self.bn1(out)
            out = self.relu1(out)

            out = self.conv2(out)
            out = self.bn2(out)

            if self.downsample is not None:
                identity = self.downsample(x)

            #! add by dongz
            out = self.torch_add(out, identity)
            # out += identity
            out = self.relu2(out)

            return out
    ```

2. Prepare your loader.
   1. Your `loader.__getitem__()` should return a tuple like `(data, label)` or `(data, index)`, qnq will use `loader.__getitem__()[0]` to forward your model.

3. Prepare pretrained checkpoints.
   1. Train your model and use `torch.save()` to save your checkpoints.
   2. Use `checkpoints = torch.load(checkpoints_path)` and `model.load_state_dict(checkpoints)` to load your checkpoints.

4. Quantize
   1. Add `from qnq import quantize`
   2. Call `quantize(model, bit_width, data_loader, path)`.

## How to eval with quantization

   1. In the program
      1. `quantize()` will turn on 'eval mode' for model, that will automatically quantize activation, and weight already be fixed-point right now.
      2. Just call your origin version `eval()`
   2. Eval `quantize.pth`
      1. Coming soon!


## How to debug

1. Call `quantize(model, bit_width, data_loader, path, is_debug=True)`.
2. Debug mode will plot every layer's stats.

## How QNQ work

Coming soon!

## Operators supported

- Convolution Layers
  - Conv
- Pooling Layers
  - AveragePool
  - AdaptiveAvgPool
- Activation
  - Relu
- Normalization Layers
  - BatchNorm
- Linear Layers
  - Linear
- Torch Function
  - Add, Minus, DotMul, MatMul, Div
  - Sin, Cos
  - SoftMax
