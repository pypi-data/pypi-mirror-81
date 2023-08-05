from tflite2onnx.op.activation import ReLU
from tflite2onnx.op.binary import Binary
from tflite2onnx.op.common import OpFactory
from tflite2onnx.op.common import Operator  # noqa: F401
from tflite2onnx.op.concat import Concat
from tflite2onnx.op.conv import Conv
from tflite2onnx.op.fullyconnected import FullyConnected
from tflite2onnx.op.padding import Padding
from tflite2onnx.op.pooling import Pooling
from tflite2onnx.op.quantize import Quantize
from tflite2onnx.op.reduce import Reduce
from tflite2onnx.op.reshape import Reshape
from tflite2onnx.op.slice import Slice
from tflite2onnx.op.softmax import Softmax
from tflite2onnx.op.split import Split
from tflite2onnx.op.transpose import Transpose
from tflite2onnx.op.unary import Unary

OpFactory.register(Binary)
OpFactory.register(Concat)
OpFactory.register(Conv)
OpFactory.register(FullyConnected)
OpFactory.register(Padding)
OpFactory.register(Pooling)
OpFactory.register(Quantize)
OpFactory.register(ReLU)
OpFactory.register(Reduce)
OpFactory.register(Reshape)
OpFactory.register(Slice)
OpFactory.register(Softmax)
OpFactory.register(Split)
OpFactory.register(Transpose)
OpFactory.register(Unary)
