# Index 1: ICG formula
def get_index_1(x):
    index = (x[:, :, 60] +
             x[:, :, 61] +
             x[:, :, 62] +
             x[:, :, 63] +
             x[:, :, 64] +
             x[:, :, 65] +
             x[:, :, 66]) / 7
    return index
