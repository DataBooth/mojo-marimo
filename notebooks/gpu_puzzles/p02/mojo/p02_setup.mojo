from gpu import thread_idx
from gpu.host import DeviceContext
from testing import assert_equal

# ANCHOR: add
comptime SIZE = 4
comptime BLOCKS_PER_GRID = 1
comptime THREADS_PER_BLOCK = SIZE
comptime dtype = DType.float32


