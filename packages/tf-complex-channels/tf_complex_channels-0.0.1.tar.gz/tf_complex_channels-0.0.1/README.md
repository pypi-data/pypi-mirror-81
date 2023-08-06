# TF Complex Channels
TF complex channels contains a set of utility tools for working with complex numbers in a channel oriented way.

This approach is proposed and described in [this blog post](https://lukewood.dev/blog/complex-deep-learning).

The primary purpose of this library and approach is to allow the community to push forward with academic research on complex number neural networks without waiting on ml library development.

##### Request for contributions
__If an operation you want is not supported, please submit an issue or open a pull request__

## Basic Usage

```python
import tf_complex_channels
print(x.dtype)
# > tf.complex64
print(x.shape)
# > (1, 2, 3)
x = complex_to_channels(x)
print(x.dtype)
# > tf.float64
print(x.shape)
# > (1, 2, 3, 2)
```

## Documentation

## Examples
