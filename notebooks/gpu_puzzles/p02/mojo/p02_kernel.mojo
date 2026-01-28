fn add(
    output: UnsafePointer[Scalar[dtype], MutAnyOrigin],
    a: UnsafePointer[Scalar[dtype], MutAnyOrigin],
    b: UnsafePointer[Scalar[dtype], MutAnyOrigin],
):
    i = thread_idx.x
    # FILL ME IN (roughly 1 line)


# ANCHOR_END: add
