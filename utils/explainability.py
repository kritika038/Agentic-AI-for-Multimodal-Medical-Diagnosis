import cv2
import numpy as np

def generate_heatmap(image):

    img = np.array(image.convert("L"))
    img = cv2.resize(img, (256, 256))
    img = cv2.GaussianBlur(img, (9, 9), 0)
    heat_source = 255 - img

    heatmap = cv2.applyColorMap(heat_source, cv2.COLORMAP_JET)
    base = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    overlay = cv2.addWeighted(base, 0.6, heatmap, 0.4, 0)

    return overlay
