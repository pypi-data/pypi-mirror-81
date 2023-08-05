from collections import OrderedDict
from collections import abc
from typing import List


class Container(abc.MutableMapping):
  def __init__(self, *args, **kwargs):
    items = OrderedDict(
      ('_arg' + str(n), v) for n, v in enumerate(args)
    )
    items.update(kwargs)

    self.__dict__.update(items)

    self._keys = list(items.keys())

    self.args = args
    self.kwargs = kwargs

  def __iter__(self):
    return (getattr(self, k) for k in self._keys)

  def __len__(self):
    return len(self._keys)

  def __getitem__(self, x):
    if isinstance(x, str):
      return getattr(self, x)
    if isinstance(x, int):
      k = self._keys[x]
      return getattr(self, k)

    if isinstance(x, slice):
      return [getattr(self, k) for k in self._keys[x]]

  def __setitem__(self, key, value):
    if isinstance(key, int):
      setattr(self, self._keys[key], value)
    elif isinstance(key, str):
      setattr(self, key, value)

  def __delitem__(self, key):
    pass


class Inputs(Container):
  pass


class Targets(Container):
  pass


class Outputs(Container):
  pass


class Samples:
  def __init__(self, inputs, targets):
    self.inputs = inputs
    self.targets = targets

  def __iter__(self):
    return (*self.inputs, *self.targets)


class Batch:
  inputs: Inputs
  targets: Targets

  def __init__(self, inputs, targets, outputs=None):
    self.inputs = inputs
    self.targets = targets

  def __iter__(self):
    return (*self.inputs, *self.targets)

  def to(self, device):
    pass

  @property
  def size(self):
    return len(self.inputs[0])


  def items(self):
    return []

class DetectionBatch(Batch):
  boxes: Inputs

class SegmentationBatch(Batch):
  masks: Inputs


batches: List[Batch] = []
for b in batches:
  b.to(model.device)
  inputs, targets = b

  outputs = model(*inputs)
  b.outputs = outputs

