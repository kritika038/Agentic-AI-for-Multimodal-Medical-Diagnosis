import numpy as np

def is_xray(image):

    img = np.array(image.convert("L"))

    mean = img.mean()
    std = img.std()

    # A lightweight heuristic based on grayscale intensity spread.
    if 40 < mean < 220 and std > 25:
        return True

    return False
