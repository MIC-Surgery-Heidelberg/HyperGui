# Example index 2
def get_index_2(x):
    index = (x[:, :, 61] +
             x[:, :, 62] +
             x[:, :, 63] +
             x[:, :, 64] +
             x[:, :, 65] +
             x[:, :, 66]) / 6
    return index
