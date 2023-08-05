"""Shows the use of annotate without any type information.
The type information is extracted from the arguments passed
and the function is annotated and compiled at runtime.
"""

from compyle.api import annotate, Elementwise, wrap, get_config, declare
import numpy as np
from numpy import sin


@annotate
def axpb(i, x, y, a, b):
    xi = x[i]
    y[i] = a * sin(xi) + b


x = np.linspace(0, 1, 10000)
y = np.zeros_like(x)
a = 2.0
b = 3.0

backend = 'opencl'
get_config().use_openmp = True
x, y = wrap(x, y, backend=backend)
e = Elementwise(axpb, backend=backend)
e(x, y, a, b)
